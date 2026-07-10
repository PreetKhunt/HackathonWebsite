# Jharkhand Tourism - Eco & Culture Platform

**Live Demo:** [https://deluxe-faloodeh-f6baed.netlify.app](https://deluxe-faloodeh-f6baed.netlify.app)

A full-stack eco and cultural tourism platform dedicated to showcasing the beauty of Jharkhand. It features a complete frontend experience with a Flask backend, Supabase database, and a fully functional suite of booking and planning tools.

## 🌟 Key Features

### 🗺️ Explore Jharkhand
Discover majestic waterfalls, dense forests, ancient heritage, and warm homestays. The platform highlights the best places to visit, including:
- **Dassam Falls & Hundru Falls**: Spectacular cascades and monsoon-favorite plunge pools.
- **Betla National Park**: Jharkhand's classic wildlife safari with elephants and the ruins of Palamu Fort.
- **Netarhat**: The 'Queen of Chotanagpur' famed for its sunrise/sunset points.
- **Patratu Valley**: Winding roads, emerald hills, and shimmering lakes.
- **Baidyanath Temple & Parasnath Hill**: Vibrant religious hubs and vital pilgrimage sites.
- **Tribal Handicrafts**: Marketplaces featuring local artisans, dokra metal crafts, and bamboo works.

### 🎭 Cultural Heritage
Immerse yourself in Jharkhand's rich traditions and vibrant communities.
- **Indigenous Heritage**: Home to 32+ tribes including Santhal, Munda, Oraon, Ho, and Kharia.
- **Artisan Crafts**: Exquisite Dokra metal casting, Paitkar painting, Sohrai art, and Tassar silk weaving.
- **Festivals**: Vibrant celebrations like Sarhul, Karam, Tusu Parab, and local village fairs.

### 🧗 Adventure & Activities
Book thrilling experiences such as:
- Trekking & Hiking (Parasnath Hill, Tagore Hill)
- Waterfall Rappelling (Dassam & Hundru Falls)
- Jungle Safaris (Betla & Palamau)
- Tribal Village Tours
- Rock Climbing & River Rafting

### 📦 Tour Packages
- **Green Getaway (Standard)**: 3D/2N perfect for backpackers with tidy stays and shared transport.
- **Mystic Trails (Deluxe)**: 5D/4N featuring 3-star hotels, guided tours, and authentic local vibes.
- **Luxury Highlands (Premium)**: 7D/6N offering private SUVs, eco-resorts/5-star stays, and curated cultural experiences.

### 💻 Platform Tools & Integrations
- **Razorpay Integration**: Fully functional payment gateway integrated into the booking workflows.
- **Booking Systems**: Seamless booking for Guides, Transport, Packages, and Activities.
- **Quick Itinerary Generator**: Generate personalized, balanced travel plans in seconds.
- **Multilingual Chatbot Assistant**: Ask about travel times, weather, places, and permits (integrated with backend AI).
- **Interactive Map**: Built with Leaflet & OpenStreetMap to pan, zoom, and explore major sites.
- **Admin Panel**: Comprehensive dashboard to manage all bookings and view statistics.

---

## 🛠️ Quick Setup (Backend)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Supabase (Optional)

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to Settings > API to get your URL and anon key
4. Run the SQL from `supabase_setup.sql` in the SQL editor

### 3. Configure Environment

Edit `.env` file (if missing, create one):
```env
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### 4. Run the Application

```bash
python app.py
```
Visit: http://localhost:5000

---

## 📁 Project Structure

```text
├── app.py                      # Flask application main file
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── supabase_setup.sql          # Database schema for Supabase
├── templates/
│   ├── index.html              # Main website template
│   ├── admin.html              # Admin dashboard
│   ├── login.html              # User login page
│   ├── signup.html             # User registration page
│   └── payment.html            # Payment processing page
└── README.md                   # This file
```

---

## 🌐 API Endpoints

### Public Routes
- `GET /` - Main website
- `GET /login` - Login page
- `GET /signup` - Registration page
- `GET /payment` - Payment page
- `GET /api/places` - Get tourist places

### Booking Services (with Razorpay integration)
- `POST /api/book-guide` - Book a guide
- `POST /api/book-transport` - Book transport
- `POST /api/book-activity` - Book activities

### AI Chatbot
- `POST /api/chat` - Chatbot responses

### Admin Panel
- `GET /admin` - Admin dashboard
- `GET /api/admin/guide-bookings` - Get guide bookings
- `GET /api/admin/transport-bookings` - Get transport bookings
- `GET /api/admin/activity-bookings` - Get activity bookings
- `GET /api/admin/stats` - Get admin statistics

---

*© 2026 Jharkhand Eco & Cultural Tourism.*
*Support: support@jharkhand-tourism.experiences | Ranchi, Jharkhand, India*