import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace data.get('email', 'guest@example.com') with user.email
old_email = "'email': data.get('email', 'guest@example.com'),"
new_email = "'email': getattr(user, 'email', data.get('email', 'guest@example.com')),"
content = content.replace(old_email, new_email)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched app.py emails!")
