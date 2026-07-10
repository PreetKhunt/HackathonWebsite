import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Inject Supabase JS and auth.js in head
head_inject = """
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="/auth.js"></script>
</head>"""
if "/auth.js" not in content:
    content = content.replace("</head>", head_inject)

# Protect bookActivity
old_ba = "function bookActivity() {"
new_ba = """async function bookActivity() {
      const session = await getSession();
      if (!session) {
        sessionStorage.setItem('redirectAfterLogin', window.location.href);
        window.location.href = '/login';
        return;
      }"""
content = content.replace(old_ba, new_ba)

# Protect bookGuide
old_bg = "function bookGuide() {"
new_bg = """async function bookGuide() {
      const session = await getSession();
      if (!session) {
        sessionStorage.setItem('redirectAfterLogin', window.location.href);
        window.location.href = '/login';
        return;
      }"""
content = content.replace(old_bg, new_bg)

# Protect bookTransport
old_bt = "function bookTransport() {"
new_bt = """async function bookTransport() {
      const session = await getSession();
      if (!session) {
        sessionStorage.setItem('redirectAfterLogin', window.location.href);
        window.location.href = '/login';
        return;
      }"""
content = content.replace(old_bt, new_bt)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched index.html!")
