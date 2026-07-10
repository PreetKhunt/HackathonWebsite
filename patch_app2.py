with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add send_file to imports if not there
if "from flask import send_file" not in content:
    content = content.replace("from flask import Flask", "from flask import Flask, send_file")

route_code = """
@app.route('/auth.js')
def serve_auth():
    return send_file('auth.js')
"""
if "@app.route('/auth.js')" not in content:
    content = content.replace("@app.route('/')", route_code + "\n@app.route('/')")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
