# Jharkhand Tourism Website - Backend Setup

A full-stack tourism website for Jharkhand with Flask backend and Supabase database.

## Features

- **Frontend**: Responsive HTML/CSS/JS with modern design
- **Backend**: Flask REST API
- **Database**: Supabase (PostgreSQL)
- **Booking System**: Guide, Transport, and Activity bookings
- **AI Chatbot**: Rule-based basic responses built-in
- **Admin Panel**: Booking management system

## Quick Setup

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
```
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

## Project Structure

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

## API Endpoints

### Public Routes
- `GET /` - Main website
- `GET /login` - Login page
- `GET /signup` - Registration page
- `GET /payment` - Payment page
- `GET /api/places` - Get tourist places

### Booking Services
- `POST /api/book-guide` - Book a guide
- `POST /api/book-transport` - Book transport
- `POST /api/book-activity` - Book activities

### AI Chatbot
- `POST /api/chat` - AI chatbot responses

### Admin Panel
- `GET /admin` - Admin dashboard
- `GET /api/admin/guide-bookings` - Get guide bookings
- `GET /api/admin/transport-bookings` - Get transport bookings
- `GET /api/admin/activity-bookings` - Get activity bookings
- `GET /api/admin/stats` - Get admin statistics

## Features Working Without Supabase

The website works even without Supabase setup by utilizing fallback functionality:
- Static places data is shown
- Booking forms show success messages
- Chatbot provides basic built-in responses