import re

with open("booking.html", "r", encoding="utf-8") as f:
    content = f.read()

head_inject = """
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="/auth.js"></script>
</head>"""
if "/auth.js" not in content:
    content = content.replace("</head>", head_inject)

old_bp = "document.getElementById('bookingForm').addEventListener('submit', async (e) => {"
new_bp = """document.getElementById('bookingForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const session = await getSession();
    if (!session) {
        sessionStorage.setItem('redirectAfterLogin', window.location.href);
        window.location.href = '/login';
        return;
    }"""
content = content.replace(old_bp, new_bp)
content = content.replace("e.preventDefault();\n    e.preventDefault();", "e.preventDefault();") # cleanup in case

with open("booking.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched booking.html!")
