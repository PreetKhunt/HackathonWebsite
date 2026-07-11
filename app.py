from flask import Flask, send_file, request, jsonify, render_template, make_response
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
app.config['SECRET_KEY'] = 'dev-secret-key'

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

# Razorpay configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

# Initialize Supabase client
supabase = None
if create_client and SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Connected to Supabase")
    except Exception as e:
        print(f"Supabase connection failed: {e}")
        print("Using fallback data")
else:
    print("Using fallback data (no Supabase config)")

# Fallback data
FALLBACK_PLACES = [
    {"name":"Dassam Falls","tag":"Waterfall","image_url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Dassam_falls.jpg/960px-Dassam_falls.jpg","description":"A spectacular cascade on the Kanchi River surrounded by sal forests."},
    {"name":"Hundru Falls","tag":"Waterfall","image_url":"https://thumbs.dreamstime.com/b/hundru-waterfalls-jharkhand-287522583.jpg","description":"Monsoon-favorite plunge pool and scenic rock formations."},
    {"name":"Betla National Park","tag":"Wildlife","image_url":"https://superbcollections.com/wp-content/uploads/2023/08/Betla-National-Park.jpeg","description":"Forests, elephants, and the ruins of Palamu Fort—Jharkhand's classic safari."},
    {"name":"Netarhat","tag":"Hill Station","image_url":"https://thumbs.dreamstime.com/b/netarhat-jharkhand-indian-view-pictures-taken-vishal-singh-170710563.jpg","description":"'Queen of Chotanagpur'—famed for sunrise/sunset points and pine avenues."}
]

# Using fallback data only


def get_current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.replace('Bearer ', '')
    if supabase:
        try:
            res = supabase.auth.get_user(token)
            return res.user
        except Exception as e:
            print(f"Auth error: {e}")
    return None

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'message': 'Unauthorized. Please log in.'}), 401
        return f(*args, **kwargs)
    return decorated


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

@app.route('/test')
def test_page():
    return render_template('test.html')

@app.route('/api/book-guide', methods=['POST'])
@require_auth
def book_guide():
    data = request.json or {}
    user = get_current_user()
    
    places_str = data.get('place', data.get('places', ''))
    if isinstance(places_str, list): places_str = ', '.join(places_str)

    booking_data = {
        'user_id': user.id,
        'name': data.get('name', 'Guest'),
        'email': getattr(user, 'email', data.get('email', 'guest@example.com')),
        'phone': data.get('phone', '0000000000'),
        'places': places_str,
        'date': data.get('date', '2025-01-01'),
        'duration': 1,
        'group_size': 1,
        'status': 'pending',
        'payment_status': 'pending'
    }
    
    if supabase:
        print(f"Incoming guide booking JSON: {booking_data}")
        mapped_data = {
            'name': booking_data.get('name', 'Unknown'),
            'email': booking_data.get('email') or (user.email if user else 'unknown@email.com'),
            'phone': booking_data.get('phone', '0000000000'),
            'places': booking_data.get('places', ''),
            'date': booking_data.get('date'),
            'duration': 1,
            'group_size': 1,
            'special_requirements': f"Language: {data.get('lang', data.get('language', ''))}",
            'user_id': user.id
        }
        print(f"Mapped guide booking data: {mapped_data}")
        try:
            res = supabase.table('guide_bookings').insert(mapped_data).execute()
            print(f"Supabase insert response: {res.data}")
            return jsonify({'success': True, 'message': 'Guide booking submitted'})
        except Exception as e:
            error_msg = str(e)
            print(f"Supabase insert failed for guide_bookings: {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 500
    return jsonify({'success': False, 'error': 'Supabase not initialized'}), 500

@app.route('/api/book-transport', methods=['POST'])
@require_auth
def book_transport():
    data = request.json or {}
    user = get_current_user()
    
    datetime_str = data.get('when', '2025-01-01T10:00')
    if 'T' in datetime_str:
        d_date, d_time = datetime_str.split('T')
    else:
        d_date, d_time = datetime_str, '10:00:00'

    booking_data = {
        'user_id': user.id,
        'name': data.get('name', 'Guest'),
        'email': getattr(user, 'email', data.get('email', 'guest@example.com')),
        'phone': data.get('phone', '0000000000'),
        'pickup_location': data.get('from', ''),
        'destination': data.get('to', ''),
        'date': d_date,
        'time': d_time,
        'passengers': 1,
        'vehicle_type': data.get('vehicle', 'sedan'),
        'status': 'pending',
        'payment_status': 'pending'
    }

    if supabase:
        print(f"Incoming transport booking JSON: {booking_data}")
        mapped_data = {
            'name': booking_data.get('name', 'Unknown'),
            'email': user.email if user else 'unknown@email.com',
            'phone': data.get('phone', booking_data.get('phone', '0000000000')),
            'pickup_location': booking_data.get('pickup_location', data.get('from', 'Unknown')),
            'destination': booking_data.get('destination', data.get('to', 'Unknown')),
            'date': d_date,
            'time': d_time,
            'passengers': 1,
            'vehicle_type': booking_data.get('vehicle_type', data.get('vehicle', 'Sedan')),
            'user_id': user.id
        }
        print(f"Mapped transport booking data: {mapped_data}")
        try:
            res = supabase.table('transport_bookings').insert(mapped_data).execute()
            print(f"Supabase insert response: {res.data}")
            return jsonify({'success': True, 'message': 'Transport booking submitted'})
        except Exception as e:
            error_msg = str(e)
            print(f"Supabase insert failed for transport_bookings: {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 500
    return jsonify({'success': False, 'error': 'Supabase not initialized'}), 500

@app.route('/api/book-activity', methods=['POST'])
@require_auth
def book_activity():
    data = request.json or {}
    user = get_current_user()
    
    booking_data = {
        'user_id': user.id,
        'name': data.get('name', 'Guest'),
        'email': getattr(user, 'email', data.get('email', 'guest@example.com')),
        'phone': data.get('phone', '0000000000'),
        'activity': data.get('activity', ''),
        'location': data.get('location', ''),
        'date': data.get('date', '2025-01-01'),
        'participants': int(data.get('participants') or 1),
        'experience_level': 'Not specified',
        'status': 'pending',
        'payment_status': 'pending'
    }

    if supabase:
        print(f"Incoming activity booking JSON: {booking_data}")
        mapped_data = {
            'name': booking_data.get('name', 'Unknown'),
            'phone': booking_data.get('phone', '0000000000'),
            'email': booking_data.get('email') or (user.email if user else 'unknown@email.com'),
            'activity': booking_data.get('activity', 'General'),
            'location': booking_data.get('location', 'Unknown'),
            'participants': int(booking_data.get('participants') or 1),
            'date': booking_data.get('date'),
            'experience_level': booking_data.get('requirements', ''),
            'user_id': user.id
        }
        print(f"Mapped activity booking data: {mapped_data}")
        try:
            res = supabase.table('activity_bookings').insert(mapped_data).execute()
            print(f"Supabase insert response: {res.data}")
            return jsonify({'success': True, 'message': 'Activity booking submitted'})
        except Exception as e:
            error_msg = str(e)
            print(f"Supabase insert failed for activity_bookings: {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 500
    return jsonify({'success': False, 'error': 'Supabase not initialized'}), 500

@app.route('/api/book-package', methods=['POST'])
@require_auth
def book_package():
    data = request.json or {}
    user = get_current_user()
    data['user_id'] = user.id
    
    # Required fields validation (optional but good practice)
    required_fields = ['name', 'email', 'phone', 'package_name', 'date', 'amount', 'payment_id', 'payment_status']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400

    if supabase:
        print(f"Incoming package booking JSON: {data}")
        mapped_data = data.copy()
        mapped_data['user_id'] = user.id if user else None
        print(f"Mapped package booking data: {mapped_data}")
        try:
            result = supabase.table('package_bookings').insert(mapped_data).execute()
            print(f"Supabase insert response: {result.data}")
            return jsonify({'success': True, 'message': 'Package booking submitted successfully', 'id': result.data[0]['id'] if result.data else None})
        except Exception as e:
            error_msg = str(e)
            print(f"Supabase insert failed for package_bookings: {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 500
    return jsonify({'success': False, 'error': 'Supabase not initialized'}), 500

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

@app.route('/api/places')
def get_places():
    if not supabase:
        return jsonify(FALLBACK_PLACES)
        
    try:
        response = supabase.table('places').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        print(f"Error fetching places: {e}")
        return jsonify(FALLBACK_PLACES)

@app.route('/api/config/razorpay')
def get_razorpay_config():
    return jsonify({'key_id': RAZORPAY_KEY_ID})


def no_cache_jsonify(*args, **kwargs):
    response = make_response(jsonify(*args, **kwargs))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/api/user/bookings')
@require_auth
def get_user_bookings():
    user = get_current_user()
    if not supabase:
        return jsonify({})
    try:
        guides = supabase.table('guide_bookings').select('*').eq('user_id', user.id).order('created_at', desc=True).execute()
        transports = supabase.table('transport_bookings').select('*').eq('user_id', user.id).order('created_at', desc=True).execute()
        activities = supabase.table('activity_bookings').select('*').eq('user_id', user.id).order('created_at', desc=True).execute()
        packages = supabase.table('package_bookings').select('*').eq('user_id', user.id).order('created_at', desc=True).execute()
        
        return no_cache_jsonify({
            'guides': guides.data or [],
            'transports': transports.data or [],
            'activities': activities.data or [],
            'packages': packages.data or []
        })
    except Exception as e:
        print(f"Error fetching user bookings: {e}")
        return no_cache_jsonify({'guides': [], 'transports': [], 'activities': [], 'packages': []})

# Admin routes
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

@app.route('/api/admin/guide-bookings')
def get_guide_bookings():
    if supabase:
        try:
            result = supabase.table('guide_bookings').select('*').order('created_at', desc=True).execute()
            return no_cache_jsonify(result.data or [])
        except Exception as e:
            print(f"Error fetching guide bookings: {e}")
    return no_cache_jsonify([])

@app.route('/api/admin/transport-bookings')
def get_transport_bookings():
    if supabase:
        try:
            result = supabase.table('transport_bookings').select('*').order('created_at', desc=True).execute()
            return no_cache_jsonify(result.data or [])
        except Exception as e:
            print(f"Error fetching transport bookings: {e}")
    return no_cache_jsonify([])

@app.route('/api/admin/activity-bookings')
def get_activity_bookings():
    if supabase:
        try:
            result = supabase.table('activity_bookings').select('*').order('created_at', desc=True).execute()
            return no_cache_jsonify(result.data or [])
        except Exception as e:
            print(f"Error fetching activity bookings: {e}")
    return no_cache_jsonify([])

@app.route('/api/admin/package-bookings')
def get_package_bookings():
    if supabase:
        try:
            result = supabase.table('package_bookings').select('*').order('created_at', desc=True).execute()
            return no_cache_jsonify(result.data or [])
        except Exception as e:
            print(f"Error fetching package bookings: {e}")
    return no_cache_jsonify([])

@app.route('/api/admin/stats')
def get_stats():
    if supabase:
        try:
            # Get total counts
            guide_total = supabase.table('guide_bookings').select('id', count='exact').execute()
            transport_total = supabase.table('transport_bookings').select('id', count='exact').execute()
            activity_total = supabase.table('activity_bookings').select('id', count='exact').execute()
            package_total = supabase.table('package_bookings').select('id', count='exact').execute()
            
            # Get today's counts
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
            print(f"Error fetching stats: {e}")
    return no_cache_jsonify({'total': {'guide': 0, 'transport': 0, 'activity': 0}, 'today': {'guide': 0, 'transport': 0, 'activity': 0}})

if __name__ == '__main__':
    app.run(debug=True)