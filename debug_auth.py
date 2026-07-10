from supabase import create_client
import os, time

url = "https://jbiovrijnxrjmpkawlgx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpiaW92cmlqbnhyam1wa2F3bGd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM2OTYzNTksImV4cCI6MjA5OTI3MjM1OX0.yONZqb3vxkv1i-riYgn_qSdt0Zgt4DHVPlBV8vf1AUU"
supabase = create_client(url, key)

email = "debug_user@example.com"
password = "TestPassword123!"

# Try to sign up
try:
    res = supabase.auth.sign_up({"email": email, "password": password})
    print("Sign up success:", res.user.email)
except Exception as e:
    print("Sign up failed (might already exist):", e)

# Try to log in
try:
    session = supabase.auth.sign_in_with_password({"email": email, "password": password})
    jwt = session.session.access_token
    print("Login success! JWT length:", len(jwt))
    with open("debug_jwt.txt", "w") as f:
        f.write(jwt)
except Exception as e:
    print("Login failed:", e)
