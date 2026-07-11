// ============================================================
//  auth.js - Supabase Authentication Helper
//  Loaded by ALL pages (index.html, booking.html, templates/*)
// ============================================================

const SUPABASE_URL = "https://jbiovrijnxrjmpkawlgx.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpiaW92cmlqbnhyam1wa2F3bGd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM2OTYzNTksImV4cCI6MjA5OTI3MjM1OX0.yONZqb3vxkv1i-riYgn_qSdt0Zgt4DHVPlBV8vf1AUU";

// Backend API base URL - used by all booking fetch() calls
window.API_BASE = 'https://hackathonwebsite-7n3a.onrender.com/api';

// Initialize Supabase client - available globally as window.supabaseClient
const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
window.supabaseClient = supabaseClient;

// ============================================================
//  Helper: Get session and attach auth header for a fetch call
//  Returns { session, headers } - call this inside every booking function.
//  DO NOT rely on a global fetch interceptor - be explicit.
// ============================================================
window.getAuthHeaders = async function() {
    const { data: { session }, error } = await window.supabaseClient.auth.getSession();
    if (error) {
        console.error("[AUTH] getSession error:", error);
    }
    console.log("[AUTH] getAuthHeaders - session exists:", !!session,
                session ? "| token length: " + session.access_token.length : "");
    const headers = { 'Content-Type': 'application/json' };
    if (session && session.access_token) {
        headers['Authorization'] = `Bearer ${session.access_token}`;
    }
    return { session, headers };
};

// ============================================================
//  Helper: Require login - redirect if not authenticated.
//  Returns session or redirects to /login.
// ============================================================
window.requireLogin = async function() {
    const { session, headers } = await window.getAuthHeaders();
    if (!session) {
        sessionStorage.setItem('redirectAfterLogin', window.location.href);
        window.location.href = '/login';
        return null;
    }
    return session;
};

// ============================================================
//  Navbar: inject auth state UI into .menu nav
// ============================================================
async function updateNavbar() {
    const navMenu = document.querySelector('.menu') || document.querySelector('nav');
    if (!navMenu) return;

    // Remove any previously injected auth items
    navMenu.querySelectorAll('.auth-nav-item').forEach(el => el.remove());

    const { data: { session } } = await window.supabaseClient.auth.getSession();
    console.log("[AUTH] updateNavbar - session:", !!session);

    if (session) {
        const user = session.user;
        const name = user.user_metadata?.name || user.email.split('@')[0];
        const initial = name.charAt(0).toUpperCase();

        const wrapper = document.createElement('div');
        wrapper.className = 'auth-nav-item';
        wrapper.style.cssText = 'position:relative;display:inline-flex;align-items:center;';
        wrapper.innerHTML = `
            <div id="navAvatarBtn" style="display:flex;align-items:center;gap:8px;padding:6px 10px;cursor:pointer;border-radius:10px;" title="${user.email}">
                <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#73d13d,#3bd1c4);color:#0b0e13;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;">${initial}</div>
                <span style="font-size:.9rem;max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${name}</span>
            </div>
            <div id="navDropdown" style="display:none;position:absolute;top:100%;right:0;background:#1b2130;border:1px solid #2b3446;border-radius:10px;min-width:180px;z-index:200;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.4);">
                <div style="padding:12px;border-bottom:1px solid #2b3446;color:#9ba3b4;font-size:0.8rem;word-break:break-all;">${user.email}</div>
                <a href="/profile" style="display:block;padding:12px 16px;color:#e7ecf3;text-decoration:none;font-size:.9rem;" onmouseover="this.style.background='#242a36'" onmouseout="this.style.background='transparent'">&#128100; My Profile</a>
                <a href="#" id="navLogoutBtn" style="display:block;padding:12px 16px;color:#ff6b6b;text-decoration:none;font-size:.9rem;" onmouseover="this.style.background='#242a36'" onmouseout="this.style.background='transparent'">&#10148; Sign Out</a>
            </div>
        `;
        navMenu.appendChild(wrapper);

        const avatarBtn = document.getElementById('navAvatarBtn');
        const dropdown = document.getElementById('navDropdown');

        avatarBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
        });
        document.addEventListener('click', () => { dropdown.style.display = 'none'; });

        document.getElementById('navLogoutBtn').addEventListener('click', async (e) => {
            e.preventDefault();
            await supabaseClient.auth.signOut();
            window.location.href = '/';
        });
    } else {
        // Show Sign In + Sign Up
        const signInLink = document.createElement('a');
        signInLink.className = 'auth-nav-item';
        signInLink.href = '/login';
        signInLink.textContent = 'Sign In';
        signInLink.style.cssText = 'font-weight:600;padding:.4rem .8rem;border-radius:10px;opacity:.9;';

        const signUpLink = document.createElement('a');
        signUpLink.className = 'auth-nav-item';
        signUpLink.href = '/signup';
        signUpLink.textContent = 'Sign Up';
        signUpLink.style.cssText = 'padding:.4rem .9rem;border-radius:10px;background:linear-gradient(135deg,#73d13d,#3bd1c4);color:#0b0e13;font-weight:700;';

        navMenu.appendChild(signInLink);
        navMenu.appendChild(signUpLink);
    }
}

// ============================================================
//  Listen for auth state changes (login, logout, token refresh)
// ============================================================
supabaseClient.auth.onAuthStateChange((event, session) => {
    console.log("[AUTH] onAuthStateChange:", event, "| session:", !!session);
    updateNavbar();
});

// ============================================================
//  On page load: update navbar + handle OAuth redirect tokens
// ============================================================
window.addEventListener('DOMContentLoaded', async () => {
    // Supabase auto-handles the hash fragment from OAuth redirect
    const { data, error } = await supabaseClient.auth.getSession();
    console.log("[AUTH] DOMContentLoaded - session:", !!data.session, error ? "| error: " + error.message : "");
    updateNavbar();
});
