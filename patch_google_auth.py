import re

# PATCH LOGIN.HTML
with open("templates/login.html", "r", encoding="utf-8") as f:
    login_html = f.read()

google_btn = """
        <div style="margin: 1.5rem 0; text-align: center; position: relative;">
            <hr style="border: 0; border-top: 1px solid #e1e5e9;">
            <span style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: white; padding: 0 10px; color: #666; font-size: 0.9rem;">or</span>
        </div>
        <button type="button" id="googleLoginBtn" class="btn btn-outline" style="background: white; border: 2px solid #e1e5e9; color: #333; display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 1rem;">
            <svg viewBox="0 0 24 24" width="20" height="20" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/><path d="M1 1h22v22H1z" fill="none"/></svg>
            Continue with Google
        </button>
"""
if 'id="googleLoginBtn"' not in login_html:
    login_html = login_html.replace('</form>', f'</form>\n{google_btn}')

forgot_pwd = """
            <div style="text-align: right; margin-top: -0.5rem; margin-bottom: 1rem;">
                <a href="#" id="forgotPwdLink" style="color: #667eea; text-decoration: none; font-size: 0.9rem;">Forgot Password?</a>
            </div>
"""
if 'id="forgotPwdLink"' not in login_html:
    login_html = login_html.replace('name="password" required minlength="6">\n            </div>', f'name="password" required minlength="6">\n            </div>{forgot_pwd}')

redirect_js = """
        // Redirect if already logged in
        getSession().then(session => {
            if (session) {
                window.location.href = '/';
            }
        });

        document.getElementById('googleLoginBtn').addEventListener('click', async () => {
            const redirectUrl = sessionStorage.getItem('redirectAfterLogin') || window.location.origin;
            await supabase.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    redirectTo: redirectUrl
                }
            });
        });

        document.getElementById('forgotPwdLink').addEventListener('click', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            if (!email) {
                showAlert('Please enter your email address first', 'error');
                return;
            }
            const { error } = await supabase.auth.resetPasswordForEmail(email, {
                redirectTo: window.location.origin + '/profile'
            });
            if (error) {
                showAlert(error.message, 'error');
            } else {
                showAlert('Password reset link sent to your email', 'success');
            }
        });
"""
if "getElementById('googleLoginBtn')" not in login_html:
    login_html = login_html.replace("document.getElementById('loginForm')", redirect_js + "\n        document.getElementById('loginForm')")

with open("templates/login.html", "w", encoding="utf-8") as f:
    f.write(login_html)


# PATCH SIGNUP.HTML
with open("templates/signup.html", "r", encoding="utf-8") as f:
    signup_html = f.read()

if 'id="googleLoginBtn"' not in signup_html:
    signup_html = signup_html.replace('</form>', f'</form>\n{google_btn}')

redirect_js_signup = """
        // Redirect if already logged in
        getSession().then(session => {
            if (session) {
                window.location.href = '/';
            }
        });

        document.getElementById('googleLoginBtn').addEventListener('click', async () => {
            const redirectUrl = sessionStorage.getItem('redirectAfterLogin') || window.location.origin;
            await supabase.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    redirectTo: redirectUrl
                }
            });
        });
"""
if "getElementById('googleLoginBtn')" not in signup_html:
    signup_html = signup_html.replace("document.getElementById('signupForm')", redirect_js_signup + "\n        document.getElementById('signupForm')")

with open("templates/signup.html", "w", encoding="utf-8") as f:
    f.write(signup_html)

print("Google Auth and Forgot Password implemented!")
