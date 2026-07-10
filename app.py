from flask import Flask, request, jsonify, render_template
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
    {"name":"Dassam Falls","tag":"Waterfall","image_url":"https://dynamic-media-cdn.tripadvisor.com/media/photo-o/19/fa/bd/6e/a-full-view-of-the-falls.jpg?w=900&h=500&s=1","description":"A spectacular cascade on the Kanchi River surrounded by sal forests."},
    {"name":"Hundru Falls","tag":"Waterfall","image_url":"https://thumbs.dreamstime.com/b/hundru-waterfalls-jharkhand-287522583.jpg","description":"Monsoon-favorite plunge pool and scenic rock formations."},
    {"name":"Betla National Park","tag":"Wildlife","image_url":"https://superbcollections.com/wp-content/uploads/2023/08/Betla-National-Park.jpeg","description":"Forests, elephants, and the ruins of Palamu Fort—Jharkhand's classic safari."},
    {"name":"Netarhat","tag":"Hill Station","image_url":"https://thumbs.dreamstime.com/b/netarhat-jharkhand-indian-view-pictures-taken-vishal-singh-170710563.jpg","description":"'Queen of Chotanagpur'—famed for sunrise/sunset points and pine avenues."}
]

# Using fallback data only

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
def book_guide():
    data = request.json or {}
    
    # Ensure required fields are present
    required_fields = ['name', 'email', 'phone', 'places', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # Add default values for optional fields
    booking_data = {
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'places': data['places'],
        'date': data['date'],
        'duration': data.get('duration', 1),
        'group_size': data.get('group_size', 1),
        'special_requirements': data.get('special_requirements', ''),
        'status': 'pending',
        'payment_status': 'pending'
    }
    
    if supabase:
        try:
            result = supabase.table('guide_bookings').insert(booking_data).execute()
            return jsonify({'success': True, 'message': 'Guide booking submitted successfully', 'id': result.data[0]['id'] if result.data else None})
        except Exception as e:
            print(f"Error saving to Supabase: {e}")
            return jsonify({'success': False, 'message': 'Failed to save booking'}), 500
    
    return jsonify({'success': True, 'message': 'Guide booking submitted successfully (fallback mode)'})

@app.route('/api/book-transport', methods=['POST'])
def book_transport():
    data = request.json or {}
    if supabase:
        try:
            supabase.table('transport_bookings').insert(data).execute()
        except Exception as e:
            print(f"Error saving to Supabase: {e}")
    return jsonify({'success': True, 'message': 'Transport booking submitted successfully'})

@app.route('/api/book-activity', methods=['POST'])
def book_activity():
    data = request.json or {}
    if supabase:
        try:
            supabase.table('activity_bookings').insert(data).execute()
        except Exception as e:
            print(f"Error saving to Supabase: {e}")
    return jsonify({'success': True, 'message': 'Activity booking submitted successfully'})

@app.route('/api/book-package', methods=['POST'])
def book_package():
    data = request.json or {}
    
    # Required fields validation (optional but good practice)
    required_fields = ['name', 'email', 'phone', 'package_name', 'date', 'amount', 'payment_id', 'payment_status']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400

    if supabase:
        try:
            result = supabase.table('package_bookings').insert(data).execute()
            return jsonify({'success': True, 'message': 'Package booking submitted successfully', 'id': result.data[0]['id'] if result.data else None})
        except Exception as e:
            print(f"Error saving to Supabase: {e}")
            return jsonify({'success': False, 'message': 'Failed to save booking'}), 500
    
    return jsonify({'success': True, 'message': 'Package booking submitted successfully (fallback mode)'})

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
    if supabase:
        try:
            result = supabase.table('places').select('*').execute()
            if result.data:
                return jsonify(result.data)
        except Exception as e:
            print(f"Error fetching from Supabase: {e}")
    return jsonify(FALLBACK_PLACES)

# Admin routes
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

@app.route('/api/admin/guide-bookings')
def get_guide_bookings():
    if supabase:
        try:
            result = supabase.table('guide_bookings').select('*').order('created_at', desc=True).execute()
            return jsonify(result.data or [])
        except Exception as e:
            print(f"Error fetching guide bookings: {e}")
    return jsonify([])

@app.route('/api/admin/transport-bookings')
def get_transport_bookings():
    if supabase:
        try:
            result = supabase.table('transport_bookings').select('*').order('created_at', desc=True).execute()
            return jsonify(result.data or [])
        except Exception as e:
            print(f"Error fetching transport bookings: {e}")
    return jsonify([])

@app.route('/api/admin/activity-bookings')
def get_activity_bookings():
    if supabase:
        try:
            result = supabase.table('activity_bookings').select('*').order('created_at', desc=True).execute()
            return jsonify(result.data or [])
        except Exception as e:
            print(f"Error fetching activity bookings: {e}")
    return jsonify([])

@app.route('/api/admin/stats')
def get_admin_stats():
    if supabase:
        try:
            # Get total counts
            guide_total = supabase.table('guide_bookings').select('id', count='exact').execute()
            transport_total = supabase.table('transport_bookings').select('id', count='exact').execute()
            activity_total = supabase.table('activity_bookings').select('id', count='exact').execute()
            
            # Get today's counts
            today = datetime.now().date().isoformat()
            guide_today = supabase.table('guide_bookings').select('id', count='exact').gte('created_at', today).execute()
            transport_today = supabase.table('transport_bookings').select('id', count='exact').gte('created_at', today).execute()
            activity_today = supabase.table('activity_bookings').select('id', count='exact').gte('created_at', today).execute()
            
            return jsonify({
                'total': {
                    'guide': guide_total.count or 0,
                    'transport': transport_total.count or 0,
                    'activity': activity_total.count or 0
                },
                'today': {
                    'guide': guide_today.count or 0,
                    'transport': transport_today.count or 0,
                    'activity': activity_today.count or 0
                }
            })
        except Exception as e:
            print(f"Error fetching stats: {e}")
    return jsonify({'total': {'guide': 0, 'transport': 0, 'activity': 0}, 'today': {'guide': 0, 'transport': 0, 'activity': 0}})

if __name__ == '__main__':
    app.run(debug=True)