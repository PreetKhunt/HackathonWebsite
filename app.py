from flask import Flask, send_file, request, jsonify, render_template, make_response, g
from flask_cors import CORS
from functools import wraps
import os
from datetime import datetime
import json

try:
    from supabase import create_client, Client
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Supabase/dotenv not installed - using fallback mode")
    create_client = None

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')          # Used ONLY for JWT verification
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')  # Used for DB inserts (bypasses RLS)

print(f"Backend SUPABASE_URL: {SUPABASE_URL}")
print(f"Backend ANON_KEY: {'SET (' + SUPABASE_ANON_KEY[:12] + '...)' if SUPABASE_ANON_KEY else 'NOT SET'}")
print(f"Backend SERVICE_KEY: {'SET (' + SUPABASE_SERVICE_KEY[:12] + '...)' if SUPABASE_SERVICE_KEY else 'NOT SET - RLS inserts WILL FAIL'}")

# Razorpay configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

# -------------------------------------------------------
# supabase_auth  : anon key  - used to verify user JWTs
# supabase_admin : service   - used for all DB operations
#   (service role bypasses RLS; auth is enforced by our
#    own require_auth decorator, NOT by RLS)
# -------------------------------------------------------
supabase_auth = None    # JWT verification client
supabase_admin = None   # DB writes client (service role)

if create_client and SUPABASE_URL:
    if SUPABASE_ANON_KEY:
        try:
            supabase_auth = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
            print("Auth client (anon key): connected")
        except Exception as e:
            print(f"Auth client failed: {e}")
    if SUPABASE_SERVICE_KEY:
        try:
            supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            print("Admin client (service role): connected")
        except Exception as e:
            print(f"Admin client failed: {e}")
    else:
        print("WARNING: SUPABASE_SERVICE_ROLE_KEY not set. DB inserts will fail RLS check.")
else:
    print("Supabase not configured - check env vars")

# Backwards-compat alias so /api/places and admin routes keep working
supabase = supabase_admin or supabase_auth


# ============================================================
#  AUTHENTICATION  - single call per request, stored in g
# ============================================================

def get_current_user():
    """
    Verify the Bearer token in the Authorization header against Supabase Auth.
    Uses the ANON KEY client (supabase_auth) to call get_user(jwt=token).
    Result is cached in flask.g so it is only called once per request.
    Returns the Supabase User object, or None if verification fails.
    """
    if hasattr(g, '_cached_user'):
        return g._cached_user

    auth_header = request.headers.get('Authorization', '')
    print(f"[AUTH] Authorization header length: {len(auth_header)}")

    if not auth_header:
        print("[AUTH] FAIL: No Authorization header")
        g._cached_user = None
        return None

    if not auth_header.startswith('Bearer '):
        print(f"[AUTH] FAIL: Does not start with 'Bearer '. Got: '{auth_header[:20]}'")
        g._cached_user = None
        return None

    token = auth_header[7:].strip()

    if not token:
        print("[AUTH] FAIL: Empty token after stripping 'Bearer '")
        g._cached_user = None
        return None

    segments = token.split('.')
    if len(segments) != 3:
        print(f"[AUTH] FAIL: Token has {len(segments)} segments (need 3). Not a valid JWT.")
        g._cached_user = None
        return None

    print(f"[AUTH] Token OK (len={len(token)}): {token[:12]}...{token[-8:]}")

    # Use the ANON key client specifically for JWT verification
    auth_client = supabase_auth or supabase_admin
    if not auth_client:
        print("[AUTH] FAIL: No Supabase client available")
        g._cached_user = None
        return None

    try:
        print("[AUTH] Calling supabase_auth.get_user(jwt=token)...")
        res = auth_client.auth.get_user(jwt=token)
        user = getattr(res, 'user', None)
        if user is None:
            print(f"[AUTH] FAIL: res.user is None. Full res: {res}")
            g._cached_user = None
            return None
        print(f"[AUTH] SUCCESS: user.id={user.id} user.email={user.email}")
        g._cached_user = user
        return user
    except Exception as e:
        print(f"[AUTH] FAIL: {type(e).__name__}: {e}")
        g._cached_user = None
        return None


def require_auth(f):
    """Decorator: verifies auth once, stores user in g.user, passes to handler."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            print(f"[AUTH] Returning 401 for {request.path}")
            return jsonify({'success': False, 'message': 'Unauthorized. Please log in.'}), 401
        g.user = user
        return f(*args, **kwargs)
    return decorated


# ============================================================
#  PAGE ROUTES
# ============================================================

@app.route('/auth.js')
def serve_auth():
    return send_file('auth.js')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/payment')
def payment_page():
    return render_template('payment.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

@app.route('/booking')
def booking_page():
    return render_template('booking.html')

@app.route('/success')
def success_page():
    return send_file('success.html')

@app.route('/test')
def test_page():
    return render_template('test.html')


# ============================================================
#  BOOKING ROUTES
# ============================================================

@app.route('/api/book-guide', methods=['POST'])
@require_auth
def book_guide():
    user = g.user   # Set by require_auth, never None here
    data = request.json or {}

    places_str = data.get('place', data.get('places', ''))
    if isinstance(places_str, list):
        places_str = ', '.join(places_str)

    mapped_data = {
        'user_id': str(user.id),
        'name': data.get('name', 'Guest'),
        'email': data.get('email') or getattr(user, 'email', 'unknown@email.com'),
        'phone': data.get('phone', '0000000000'),
        'places': places_str,
        'date': data.get('date', '2025-01-01'),
        'duration': int(data.get('duration', 1)),
        'group_size': int(data.get('group_size', 1)),
        'special_requirements': f"Language: {data.get('lang', data.get('language', ''))}",
    }

    print(f"[GUIDE] user_id={str(user.id)} | payload={json.dumps(mapped_data, default=str)}")

    if not supabase_admin:
        return jsonify({'success': False, 'error': 'Service role client not initialized (check SUPABASE_SERVICE_ROLE_KEY env var)'}), 500

    try:
        res = supabase_admin.table('guide_bookings').insert(mapped_data).execute()
        print(f"[GUIDE] Insert OK: {res.data}")
        return jsonify({'success': True, 'message': 'Guide booking submitted successfully'})
    except Exception as e:
        print(f"[GUIDE] Insert FAILED: {type(e).__name__}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/book-transport', methods=['POST'])
@require_auth
def book_transport():
    user = g.user
    data = request.json or {}

    datetime_str = data.get('when', '2025-01-01T10:00')
    if 'T' in str(datetime_str):
        parts = datetime_str.split('T')
        d_date, d_time = parts[0], parts[1] if len(parts) > 1 else '10:00'
    else:
        d_date, d_time = datetime_str, '10:00'

    mapped_data = {
        'user_id': str(user.id),
        'name': data.get('name', 'Guest'),
        'email': data.get('email') or getattr(user, 'email', 'unknown@email.com'),
        'phone': data.get('phone', '0000000000'),
        'pickup_location': data.get('from', ''),
        'destination': data.get('to', ''),
        'date': d_date,
        'time': d_time,
        'passengers': int(data.get('passengers', 1)),
        'vehicle_type': data.get('vehicle', 'Sedan'),
    }

    print(f"[TRANSPORT] user_id={str(user.id)} | payload={json.dumps(mapped_data, default=str)}")

    if not supabase_admin:
        return jsonify({'success': False, 'error': 'Service role client not initialized'}), 500

    try:
        res = supabase_admin.table('transport_bookings').insert(mapped_data).execute()
        print(f"[TRANSPORT] Insert OK: {res.data}")
        return jsonify({'success': True, 'message': 'Transport booking submitted successfully'})
    except Exception as e:
        print(f"[TRANSPORT] Insert FAILED: {type(e).__name__}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/book-activity', methods=['POST'])
@require_auth
def book_activity():
    user = g.user
    data = request.json or {}

    mapped_data = {
        'user_id': str(user.id),
        'name': data.get('name', 'Guest'),
        'email': data.get('email') or getattr(user, 'email', 'unknown@email.com'),
        'phone': data.get('phone', '0000000000'),
        'activity': data.get('activity', 'General'),
        'location': data.get('location', ''),
        'date': data.get('date', '2025-01-01'),
        'participants': int(data.get('participants') or 1),
        'experience_level': data.get('requirements', ''),
    }

    print(f"[ACTIVITY] user_id={str(user.id)} | payload={json.dumps(mapped_data, default=str)}")

    if not supabase_admin:
        return jsonify({'success': False, 'error': 'Service role client not initialized'}), 500

    try:
        res = supabase_admin.table('activity_bookings').insert(mapped_data).execute()
        print(f"[ACTIVITY] Insert OK: {res.data}")
        return jsonify({'success': True, 'message': 'Activity booking submitted successfully'})
    except Exception as e:
        print(f"[ACTIVITY] Insert FAILED: {type(e).__name__}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/book-package', methods=['POST'])
@require_auth
def book_package():
    user = g.user
    data = request.json or {}

    required_fields = ['name', 'email', 'phone', 'package_name', 'date', 'amount', 'payment_id', 'payment_status']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400

    mapped_data = {
        'user_id': str(user.id),
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'package_name': data['package_name'],
        'date': data['date'],
        'amount': float(data['amount']),
        'payment_id': data['payment_id'],
        'payment_status': data['payment_status'],
        'adults': int(data.get('adults', 1)),
        'children': int(data.get('children', 0)),
        'city': data.get('city', ''),
        'state': data.get('state', ''),
        'country': data.get('country', 'India'),
        'special_requests': data.get('special_requests', ''),
    }

    print(f"[PACKAGE] user_id={str(user.id)} | payload={json.dumps(mapped_data, default=str)}")

    if not supabase_admin:
        return jsonify({'success': False, 'error': 'Service role client not initialized'}), 500

    try:
        result = supabase_admin.table('package_bookings').insert(mapped_data).execute()
        print(f"[PACKAGE] Insert OK: {result.data}")
        booking_id = result.data[0]['id'] if result.data else None
        return jsonify({'success': True, 'message': 'Package booking submitted successfully', 'id': booking_id})
    except Exception as e:
        print(f"[PACKAGE] Insert FAILED: {type(e).__name__}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
#  PLACES & CHAT
# ============================================================

FALLBACK_PLACES = [
    {"name": "Dassam Falls", "tag": "Waterfall", "image_url": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/19/fa/bd/6e/a-full-view-of-the-falls.jpg?w=900&h=500&s=1", "description": "A spectacular cascade on the Kanchi River surrounded by sal forests."},
    {"name": "Hundru Falls", "tag": "Waterfall", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Hundru_Falls.jpg/1200px-Hundru_Falls.jpg", "description": "Monsoon-favorite plunge pool and scenic rock formations."},
    {"name": "Betla National Park", "tag": "Wildlife", "image_url": "https://superbcollections.com/wp-content/uploads/2023/08/Betla-National-Park.jpeg", "description": "Forests, elephants, and the ruins of Palamu Fort."},
    {"name": "Netarhat", "tag": "Hill Station", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Netarhat_Hill_Station.jpg/1200px-Netarhat_Hill_Station.jpg", "description": "'Queen of Chotanagpur'—famed for sunrise/sunset points."}
]


@app.route('/api/places')
def get_places():
    if not supabase:
        return jsonify(FALLBACK_PLACES)
    try:
        response = supabase.table('places').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        print(f"[PLACES] Error fetching places: {e}")
        return jsonify(FALLBACK_PLACES)


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    question = data.get('question', '').lower()
    if 'weather' in question:
        response = "The weather in Jharkhand is generally pleasant. Currently around 25°C."
    elif 'place' in question:
        response = "Popular places: Dassam Falls, Betla National Park, Hundru Falls, Netarhat."
    else:
        response = "Ask about Jharkhand weather, places, travel times, or activities!"
    return jsonify({'response': response})


@app.route('/api/config/razorpay')
def get_razorpay_config():
    return jsonify({'key_id': RAZORPAY_KEY_ID})


# ============================================================
#  USER PROFILE / BOOKINGS
# ============================================================

def no_cache_jsonify(*args, **kwargs):
    response = make_response(jsonify(*args, **kwargs))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/api/user/bookings')
@require_auth
def get_user_bookings():
    user = g.user
    if not supabase:
        return no_cache_jsonify({'guides': [], 'transports': [], 'activities': [], 'packages': []})
    try:
        guides = supabase.table('guide_bookings').select('*').eq('user_id', str(user.id)).order('created_at', desc=True).execute()
        transports = supabase.table('transport_bookings').select('*').eq('user_id', str(user.id)).order('created_at', desc=True).execute()
        activities = supabase.table('activity_bookings').select('*').eq('user_id', str(user.id)).order('created_at', desc=True).execute()
        packages = supabase.table('package_bookings').select('*').eq('user_id', str(user.id)).order('created_at', desc=True).execute()
        return no_cache_jsonify({
            'guides': guides.data or [],
            'transports': transports.data or [],
            'activities': activities.data or [],
            'packages': packages.data or []
        })
    except Exception as e:
        print(f"[PROFILE] Error fetching user bookings: {e}")
        return no_cache_jsonify({'guides': [], 'transports': [], 'activities': [], 'packages': []})


# ============================================================
#  ADMIN ROUTES
# ============================================================

@app.route('/api/admin/guide-bookings')
def get_guide_bookings():
    if supabase:
        try:
            result = supabase.table('guide_bookings').select('*').order('created_at', desc=True).execute()
            return no_cache_jsonify(result.data or [])
        except Exception as e:
            print(f"[ADMIN] Error fetching guide bookings: {e}")
    return no_cache_jsonify([])


@app.route('/api/admin/transport-bookings')
def get_transport_bookings():
    if supabase:
        try:
            result = supabase.table('transport_bookings').select('*').order('created_at', desc=True).execute()
            return no_cache_jsonify(result.data or [])
        except Exception as e:
            print(f"[ADMIN] Error fetching transport bookings: {e}")
    return no_cache_jsonify([])


@app.route('/api/admin/activity-bookings')
def get_activity_bookings():
    if supabase:
        try:
            result = supabase.table('activity_bookings').select('*').order('created_at', desc=True).execute()
            return no_cache_jsonify(result.data or [])
        except Exception as e:
            print(f"[ADMIN] Error fetching activity bookings: {e}")
    return no_cache_jsonify([])


@app.route('/api/admin/package-bookings')
def get_package_bookings():
    if supabase:
        try:
            result = supabase.table('package_bookings').select('*').order('created_at', desc=True).execute()
            return no_cache_jsonify(result.data or [])
        except Exception as e:
            print(f"[ADMIN] Error fetching package bookings: {e}")
    return no_cache_jsonify([])


@app.route('/api/admin/stats')
def get_stats():
    if supabase:
        try:
            guide_total = supabase.table('guide_bookings').select('id', count='exact').execute()
            transport_total = supabase.table('transport_bookings').select('id', count='exact').execute()
            activity_total = supabase.table('activity_bookings').select('id', count='exact').execute()
            package_total = supabase.table('package_bookings').select('id', count='exact').execute()

            today = datetime.now().date().isoformat()
            guide_today = supabase.table('guide_bookings').select('id', count='exact').gte('created_at', today).execute()
            transport_today = supabase.table('transport_bookings').select('id', count='exact').gte('created_at', today).execute()
            activity_today = supabase.table('activity_bookings').select('id', count='exact').gte('created_at', today).execute()
            package_today = supabase.table('package_bookings').select('id', count='exact').gte('created_at', today).execute()

            return no_cache_jsonify({
                'total': {
                    'guide': guide_total.count or 0,
                    'transport': transport_total.count or 0,
                    'activity': activity_total.count or 0,
                    'package': package_total.count or 0
                },
                'today': {
                    'guide': guide_today.count or 0,
                    'transport': transport_today.count or 0,
                    'activity': activity_today.count or 0,
                    'package': package_today.count or 0
                }
            })
        except Exception as e:
            print(f"[ADMIN] Error fetching stats: {e}")
    return no_cache_jsonify({'total': {'guide': 0, 'transport': 0, 'activity': 0, 'package': 0},
                             'today': {'guide': 0, 'transport': 0, 'activity': 0, 'package': 0}})


if __name__ == '__main__':
    app.run(debug=True)