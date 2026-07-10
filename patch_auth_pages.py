import re

# PATCH LOGIN
with open("templates/login.html", "r", encoding="utf-8") as f:
    login_html = f.read()

head_inject = """
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="/auth.js"></script>
</head>"""
if "/auth.js" not in login_html:
    login_html = login_html.replace("</head>", head_inject)

old_login_js = """            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert('Login successful! Redirecting...', 'success');
                    localStorage.setItem('access_token', result.access_token);
                    localStorage.setItem('user_name', result.user);
                    setTimeout(() => window.location.href = '/', 1500);
                } else {
                    showAlert(result.error || 'Login failed', 'error');
                }
            } catch (error) {
                showAlert('Network error. Please try again.', 'error');
            }"""

new_login_js = """            try {
                const { data: authData, error } = await supabase.auth.signInWithPassword({
                    email: data.email,
                    password: data.password
                });
                
                if (error) {
                    showAlert(error.message || 'Login failed', 'error');
                } else {
                    showAlert('Login successful! Redirecting...', 'success');
                    setTimeout(() => {
                        const redirectUrl = sessionStorage.getItem('redirectAfterLogin') || '/';
                        sessionStorage.removeItem('redirectAfterLogin');
                        window.location.href = redirectUrl;
                    }, 1500);
                }
            } catch (error) {
                showAlert('Network error. Please try again.', 'error');
            }"""
login_html = login_html.replace(old_login_js, new_login_js)

with open("templates/login.html", "w", encoding="utf-8") as f:
    f.write(login_html)


# PATCH SIGNUP
with open("templates/signup.html", "r", encoding="utf-8") as f:
    signup_html = f.read()

if "/auth.js" not in signup_html:
    signup_html = signup_html.replace("</head>", head_inject)

old_signup_js = """            try {
                const response = await fetch('/api/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert('Account created successfully! Redirecting to login...', 'success');
                    setTimeout(() => window.location.href = '/login', 2000);
                } else {
                    showAlert(result.error || 'Signup failed', 'error');
                }
            } catch (error) {
                showAlert('Network error. Please try again.', 'error');
            }"""

new_signup_js = """            try {
                const { data: authData, error } = await supabase.auth.signUp({
                    email: data.email,
                    password: data.password,
                    options: {
                        data: {
                            name: data.name
                        }
                    }
                });
                
                if (error) {
                    showAlert(error.message || 'Signup failed', 'error');
                } else {
                    showAlert('Account created successfully! Redirecting to home...', 'success');
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                }
            } catch (error) {
                showAlert('Network error. Please try again.', 'error');
            }"""
signup_html = signup_html.replace(old_signup_js, new_signup_js)

with open("templates/signup.html", "w", encoding="utf-8") as f:
    f.write(signup_html)

print("Patched auth pages!")
