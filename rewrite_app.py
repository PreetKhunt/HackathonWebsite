import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add make_response to imports
if "from flask import make_response" not in content:
    content = content.replace("from flask import Flask, request, jsonify, render_template", "from flask import Flask, request, jsonify, render_template, make_response")

# Add the helper function
helper = """
def no_cache_jsonify(*args, **kwargs):
    response = make_response(jsonify(*args, **kwargs))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

"""
if "def no_cache_jsonify" not in content:
    content = content.replace("# Admin routes", helper + "# Admin routes")


def replace_admin_route(content, route_name, table_name):
    pattern = rf"@app\.route\('/api/admin/{route_name}'\)\ndef get_{route_name.replace('-', '_')}\(\):\n    if supabase:\n        try:\n            result = supabase\.table\('{table_name}'\)\.select\('\*'\)\.order\('created_at', desc=True\)\.execute\(\)\n            return jsonify\(result\.data or \[\]\)\n        except Exception as e:\n            print\(f\"Error fetching {route_name.replace('-', ' ')}: {{e}}\"\)\n    return jsonify\(\[\]\)"
    
    replacement = f"""@app.route('/api/admin/{route_name}')
def get_{route_name.replace('-', '_')}():
    if supabase:
        try:
            print(f"Fetching fresh {table_name} from Supabase...")
            result = supabase.table('{table_name}').select('*').order('created_at', desc=True).execute()
            print(f"Fetch {table_name} result: {{result.data}}")
            return no_cache_jsonify(result.data or [])
        except Exception as e:
            print(f"Error fetching {route_name.replace('-', ' ')}: {{e}}")
    return no_cache_jsonify([])"""
    
    return re.sub(pattern, replacement, content)

content = replace_admin_route(content, "guide-bookings", "guide_bookings")
content = replace_admin_route(content, "transport-bookings", "transport_bookings")
content = replace_admin_route(content, "activity-bookings", "activity_bookings")
content = replace_admin_route(content, "package-bookings", "package_bookings")

def replace_insert_route(content, route_name, table_name, func_name, var_name):
    # This is a bit tricky with regex, so let's just do a string replace on the try block
    old_try = f"""        try:
            supabase.table('{table_name}').insert({var_name}).execute()
        except Exception as e:"""
    
    new_try = f"""        try:
            print(f"Incoming request to {route_name}: {{{var_name}}}")
            res = supabase.table('{table_name}').insert({var_name}).execute()
            print(f"Supabase insert result for {table_name}: {{res.data}}")
        except Exception as e:"""
    
    return content.replace(old_try, new_try)

content = replace_insert_route(content, "/api/book-guide", "guide_bookings", "book_guide", "booking_data")
content = replace_insert_route(content, "/api/book-transport", "transport_bookings", "book_transport", "booking_data")
content = replace_insert_route(content, "/api/book-activity", "activity_bookings", "book_activity", "booking_data")

# Package booking has a slightly different try block
old_pkg_try = """        try:
            result = supabase.table('package_bookings').insert(data).execute()
            return jsonify({'success': True, 'message': 'Package booking submitted successfully', 'id': result.data[0]['id'] if result.data else None})
        except Exception as e:"""

new_pkg_try = """        try:
            print(f"Incoming request to /api/book-package: {data}")
            result = supabase.table('package_bookings').insert(data).execute()
            print(f"Supabase insert result for package_bookings: {result.data}")
            return jsonify({'success': True, 'message': 'Package booking submitted successfully', 'id': result.data[0]['id'] if result.data else None})
        except Exception as e:"""
content = content.replace(old_pkg_try, new_pkg_try)

# Replace the stats admin route to also use no_cache_jsonify
content = content.replace("return jsonify({\n                'total':", "return no_cache_jsonify({\n                'total':")
content = content.replace("return jsonify({'total': {'guide': 0, 'transport': 0, 'activity': 0}, 'today': {'guide': 0, 'transport': 0, 'activity': 0}})", "return no_cache_jsonify({'total': {'guide': 0, 'transport': 0, 'activity': 0}, 'today': {'guide': 0, 'transport': 0, 'activity': 0}})")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated app.py!")
