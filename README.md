# Jharkhand Tourism - Eco & Culture Platform

**Live Demo:** [https://tourismwe.netlify.app](https://tourismwe.netlify.app)
**Backend API:** [https://hackathonwebsite-7n3a.onrender.com](https://hackathonwebsite-7n3a.onrender.com)

A full-stack eco and cultural tourism platform dedicated to showcasing the beauty of Jharkhand. It features a complete decoupled frontend experience hosted on Netlify with a Flask backend hosted on Render, Supabase for authentication and database management, and a fully functional suite of booking and planning tools.

---

## 🌟 Key Features

### 🗺️ Explore Jharkhand
Discover majestic waterfalls, dense forests, ancient heritage, and warm homestays. The platform highlights the best places to visit, including:
- **Dassam Falls & Hundru Falls**: Spectacular cascades and monsoon-favorite plunge pools.
- **Betla National Park**: Jharkhand's classic wildlife safari with elephants and the ruins of Palamu Fort.
- **Netarhat**: The 'Queen of Chotanagpur' famed for its sunrise/sunset points.
- **Patratu Valley**: Winding roads, emerald hills, and shimmering lakes.
- **Baidyanath Temple & Parasnath Hill**: Vibrant religious hubs and vital pilgrimage sites.

### 🎭 Cultural Heritage
Immerse yourself in Jharkhand's rich traditions and vibrant communities.
- **Indigenous Heritage**: Home to 32+ tribes including Santhal, Munda, Oraon, Ho, and Kharia.
- **Artisan Crafts**: Exquisite Dokra metal casting, Paitkar painting, Sohrai art, and Tassar silk weaving.
- **Festivals**: Vibrant celebrations like Sarhul, Karam, and Tusu Parab.

### 🧗 Adventure & Activities
Book thrilling experiences such as:
- Trekking & Hiking (Parasnath Hill, Tagore Hill)
- Waterfall Rappelling (Dassam & Hundru Falls)
- Jungle Safaris (Betla & Palamau)

### 📦 Tour Packages
- **Green Getaway (Standard)**: 3D/2N perfect for backpackers.
- **Mystic Trails (Deluxe)**: 5D/4N featuring 3-star hotels and guided tours.
- **Luxury Highlands (Premium)**: 7D/6N offering private SUVs and eco-resorts.

### 💻 Platform Tools & Integrations
- **Authentication**: JWT-based authentication using Supabase Auth, securing user dashboards and booking APIs.
- **Role-Based Access Control**: Secure Admin dashboard accessible only to authorized administrators (`khuntpreet12@gmail.com`).
- **Booking Systems**: Seamlessly authenticated booking APIs for Guides, Transport, Packages, and Activities.
- **Razorpay Integration**: Fully functional mock payment gateway integrated into the package booking workflows.
- **Quick Itinerary Generator**: Generate personalized, balanced travel plans in seconds.
- **Multilingual Chatbot Assistant**: Ask about travel times, weather, places, and permits (integrated with backend AI).
- **Interactive Map**: Built with Leaflet & OpenStreetMap to pan, zoom, and explore major sites.

---

## 🏗️ Technical Architecture

The platform follows a decoupled architecture, separating the static frontend from the API-driven backend:

- **Frontend (Netlify)**: HTML, CSS, Vanilla JavaScript. Uses `_redirects` for clean URL routing (e.g., `/login` mapping to `/templates/login.html`). Interacts directly with Supabase for user session management via the Supabase JS v2 SDK.
- **Backend (Render)**: Python Flask API served via Gunicorn. Enforces JWT token validation via `@require_auth` decorators.
- **Database & Auth (Supabase)**: PostgreSQL database utilizing Row Level Security (RLS).
  - The frontend uses the `SUPABASE_ANON_KEY` to authenticate users and generate JWTs.
  - The backend uses the `SUPABASE_SERVICE_ROLE_KEY` to perform secure database inserts, bypassing RLS while enforcing its own application-level JWT authorization.

---

## 🚀 Deployment

The project is continuously deployed across two platforms:

### 1. Frontend (Netlify)
- Configured to serve static assets directly from the repository.
- Uses `netlify.toml` and `_redirects` for resolving SPA-like clean URLs to their respective HTML templates.
- **URL**: `https://tourismwe.netlify.app`

### 2. Backend (Render)
- Configured as a Python Web Service running `app.py`.
- **Command**: `gunicorn app:app`
- Contains environment variables securely injected for Supabase (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`) and Razorpay.
- **URL**: `https://hackathonwebsite-7n3a.onrender.com`

---

## 🛠️ Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/PreetKhunt/HackathonWebsite.git
cd HackathonWebsite
```

### 2. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
```

### 4. Run the Flask Server
```bash
python app.py
```
The server will start at `http://127.0.0.1:5000`.

*(Note: During local development, the Flask app can serve the frontend templates natively via `render_template`. In production, Netlify handles the static file serving and makes cross-origin requests to the Render API.)*

---

## 🔐 Authentication & Security

- **Supabase JS Client**: The frontend uses `window.supabaseClient` in `auth.js` to handle Sign Up, Login, and Session management.
- **API Protection**: API requests that mutate data (like Bookings) extract the `access_token` from the Supabase session and include it in the `Authorization: Bearer <token>` header.
- **Backend Validation**: Flask verifies the JWT using `supabase_auth.auth.get_user(jwt=token)`. If valid, the booking is inserted via the `supabase_admin` (service role) client to bypass strict RLS inserts, guaranteeing that only validated users can create records.
- **Admin Endpoints**: Endpoints like `/api/admin/stats` and `/api/admin/*-bookings` are strictly protected by a `@require_admin` decorator.

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request