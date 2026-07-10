import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add wraps to imports
if "from functools import wraps" not in content:
    content = content.replace("from flask import Flask, request, jsonify, render_template, make_response", "from flask import Flask, request, jsonify, render_template, make_response\nfrom functools import wraps")

# Add authentication helper
auth_helper = """
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
"""
if "def get_current_user():" not in content:
    content = content.replace("@app.route('/')", auth_helper + "\n@app.route('/')")

# Protect booking routes
# 1. book_guide
old_bg = """@app.route('/api/book-guide', methods=['POST'])
def book_guide():
    data = request.json or {}"""
new_bg = """@app.route('/api/book-guide', methods=['POST'])
@require_auth
def book_guide():
    data = request.json or {}
    user = get_current_user()"""
content = content.replace(old_bg, new_bg)

old_bg_data = """    booking_data = {
        'name': data.get('name', 'Guest'),"""
new_bg_data = """    booking_data = {
        'user_id': user.id,
        'name': data.get('name', 'Guest'),"""
content = content.replace(old_bg_data, new_bg_data)

# 2. book_transport
old_bt = """@app.route('/api/book-transport', methods=['POST'])
def book_transport():
    data = request.json or {}"""
new_bt = """@app.route('/api/book-transport', methods=['POST'])
@require_auth
def book_transport():
    data = request.json or {}
    user = get_current_user()"""
content = content.replace(old_bt, new_bt)

old_bt_data = """    booking_data = {
        'name': data.get('name', 'Guest'),"""
content = content.replace(old_bt_data, new_bg_data)

# 3. book_activity
old_ba = """@app.route('/api/book-activity', methods=['POST'])
def book_activity():
    data = request.json or {}"""
new_ba = """@app.route('/api/book-activity', methods=['POST'])
@require_auth
def book_activity():
    data = request.json or {}
    user = get_current_user()"""
content = content.replace(old_ba, new_ba)

old_ba_data = """    booking_data = {
        'name': data.get('name', 'Guest'),"""
content = content.replace(old_ba_data, new_bg_data)

# 4. book_package
old_bp = """@app.route('/api/book-package', methods=['POST'])
def book_package():
    data = request.json or {}"""
new_bp = """@app.route('/api/book-package', methods=['POST'])
@require_auth
def book_package():
    data = request.json or {}
    user = get_current_user()
    data['user_id'] = user.id"""
content = content.replace(old_bp, new_bp)


# Add Profile routes
profile_routes = """
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
"""
if "@app.route('/api/user/bookings')" not in content:
    content = content.replace("# Admin routes", profile_routes + "\n# Admin routes")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched app.py successfully!")
