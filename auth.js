// Supabase Authentication Helper for Frontend
const SUPABASE_URL = "https://jbiovrijnxrjmpkawlgx.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpiaW92cmlqbnhyam1wa2F3bGd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM2OTYzNTksImV4cCI6MjA5OTI3MjM1OX0.yONZqb3vxkv1i-riYgn_qSdt0Zgt4DHVPlBV8vf1AUU";

const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Helper to get current session
async function getSession() {
    const { data, error } = await supabaseClient.auth.getSession();
    if (error) console.error("Error getting session:", error);
    return data.session;
}

// Intercept fetch requests to add Authorization header automatically
const originalFetch = window.fetch;
window.fetch = async function() {
    let [resource, config] = arguments;
    
    // Check if the request is destined for our backend API
    const isApiRequest = typeof resource === 'string' && (
        resource.startsWith('/api/') || 
        (window.API_BASE && resource.startsWith(window.API_BASE))
    );
    
    if (isApiRequest) {
        const session = await getSession();
        if (session) {
            config = config || {};
            config.headers = config.headers || {};
            config.headers['Authorization'] = `Bearer ${session.access_token}`;
        }
    }
    return originalFetch(resource, config);
};

// Check auth and redirect if not logged in (used on protected pages)
async function requireAuth() {
    const session = await getSession();
    if (!session) {
        sessionStorage.setItem('redirectAfterLogin', window.location.href);
        window.location.href = 'templates/login.html';
        return null;
    }
    return session.user;
}

// Update Navbar UI based on auth state
async function updateNavbar() {
    const session = await getSession();
    console.log("Supabase Auth Session (updateNavbar):", session);
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    
    // Remove existing auth links to replace them
    const existingAuth = document.querySelectorAll('.auth-nav-item');
    existingAuth.forEach(el => el.remove());
    
    if (session) {
        const user = session.user;
        const name = user.user_metadata?.name || user.email.split('@')[0];
        
        const profileDropdown = document.createElement('div');
        profileDropdown.className = 'auth-nav-item dropdown';
        profileDropdown.style.position = 'relative';
        profileDropdown.style.display = 'inline-block';
        profileDropdown.style.cursor = 'pointer';
        profileDropdown.innerHTML = `
            <div style="display:flex;align-items:center;gap:8px;padding:8px;">
                <div style="width:32px;height:32px;border-radius:50%;background:#667eea;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;">
                    ${name.charAt(0).toUpperCase()}
                </div>
                <span>${name}</span>
            </div>
            <div class="dropdown-content" style="display:none;position:absolute;right:0;background:white;box-shadow:0 8px 16px rgba(0,0,0,0.1);min-width:160px;z-index:100;border-radius:4px;">
                <div style="padding:12px;border-bottom:1px solid #eee;color:#666;font-size:0.9em;">${user.email}</div>
                <a href="templates/profile.html" style="display:block;padding:12px;color:#333;text-decoration:none;">My Profile</a>
                <a href="#" id="logoutBtn" style="display:block;padding:12px;color:#d32f2f;text-decoration:none;">Logout</a>
            </div>
        `;
        
        navLinks.appendChild(profileDropdown);
        
        profileDropdown.addEventListener('mouseenter', () => profileDropdown.querySelector('.dropdown-content').style.display = 'block');
        profileDropdown.addEventListener('mouseleave', () => profileDropdown.querySelector('.dropdown-content').style.display = 'none');
        
        document.getElementById('logoutBtn').addEventListener('click', async (e) => {
            e.preventDefault();
            await supabaseClient.auth.signOut();
            window.location.href = 'index.html';
        });
    } else {
        const loginLink = document.createElement('a');
        loginLink.className = 'auth-nav-item';
        loginLink.href = '/login';
        loginLink.textContent = 'Sign In';
        loginLink.style.fontWeight = 'bold';
        
        const signupLink = document.createElement('a');
        signupLink.className = 'auth-nav-item';
        signupLink.href = 'templates/signup.html';
        signupLink.textContent = 'Sign Up';
        signupLink.style.padding = '8px 16px';
        signupLink.style.background = '#667eea';
        signupLink.style.color = 'white';
        signupLink.style.borderRadius = '4px';
        
        navLinks.appendChild(loginLink);
        navLinks.appendChild(signupLink);
    }
}

// Function to handle booking button clicks
async function handleBookingClick(e, bookingFunction) {
    e.preventDefault();
    const session = await getSession();
    if (!session) {
        // Save current scroll or context if needed, then redirect
        sessionStorage.setItem('redirectAfterLogin', window.location.href);
        window.location.href = 'templates/login.html';
    } else {
        bookingFunction();
    }
}

// Listen for auth state changes to update UI instantly
supabaseClient.auth.onAuthStateChange((event, session) => {
    console.log("onAuthStateChange event:", event, "session:", session);
    updateNavbar();
});

// Immediately parse session on load for OAuth callbacks
window.addEventListener('load', async () => {
    const { data, error } = await supabaseClient.auth.getSession();
    console.log("Session check on page load:", data.session, "Error:", error);
    if (error) {
        console.error("OAuth callback/session error:", error);
    }
});
window.API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? 'http://127.0.0.1:5000/api' : 'https://tourismwe-backend.onrender.com/api';
