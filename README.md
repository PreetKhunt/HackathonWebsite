# Jharkhand Tourism

A tourism website for discovering Jharkhand destinations, browsing tour packages, and booking travel services. The frontend is served as static HTML on Netlify; a Flask API on Render handles authentication-protected bookings and integrates Supabase and Razorpay.

- **Website:** https://tourismwe.netlify.app
- **API:** https://hackathonwebsite-7n3a.onrender.com

## Features

- Destination listings, cultural information, maps, itinerary planning, and a keyword-based travel chatbot.
- Supabase Auth sign-in and registration.
- Authenticated guide, transport, activity, and package booking workflows.
- Razorpay package checkout: the API sets package prices, creates orders, verifies payment signatures, captures authorized payments, and saves confirmed bookings.
- User profile and booking history, plus protected admin booking and statistics endpoints.

## Technology

- **Frontend:** HTML, CSS, and vanilla JavaScript; Supabase JavaScript client v2.
- **Backend:** Python 3 and Flask, served with Gunicorn.
- **Database and authentication:** Supabase.
- **Payments:** Razorpay Checkout and the Razorpay Python SDK.
- **Hosting:** Netlify (frontend) and Render (backend).

## Run locally

### Requirements

- Python 3.10 or newer
- A Supabase project
- Razorpay API credentials (use Test Mode while developing)

### Install and configure

```powershell
git clone https://github.com/PreetKhunt/HackathonWebsite.git
cd HackathonWebsite
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY=YOUR_SUPABASE_SERVICE_ROLE_KEY
RAZORPAY_KEY_ID=YOUR_RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET=YOUR_RAZORPAY_KEY_SECRET
```

Keep `.env` and all service-role/payment secrets out of Git. The service-role key and Razorpay secret belong only on the backend. The browser receives the Razorpay key ID, never the key secret.

Start the Flask app:

```powershell
python app.py
```

The local Flask server is available at `http://127.0.0.1:5000`. It serves templates for the home, login, signup, profile, admin, and booking pages. The frontend's API base is configured in [`auth.js`](./auth.js); for a fully local flow, point `window.API_BASE` at `http://127.0.0.1:5000/api` instead of the deployed API.

## Package payment flow

1. Select a package and submit the booking form while signed in.
2. The browser requests an authenticated order from `POST /api/create-razorpay-order`.
3. The backend selects the price from its package catalog and creates the Razorpay order. The browser-supplied price is not used to charge the customer.
4. Razorpay Checkout returns the order ID, payment ID, and signature.
5. `POST /api/book-package` verifies the signature and checks the order, user, package, amount, and currency against Razorpay. Authorized payments are captured before the booking is saved.
6. Only a verified, captured payment is recorded as paid.

The package catalog is maintained in `app.py` (`Budget`, `Deluxe`, and `Premium`). Keep the package links and catalog in sync when changing prices. Test payments require Razorpay Test Mode credentials; switch to live credentials only when ready to accept real charges.

## API overview

All API routes are under `/api`. Booking and user-specific routes require a Supabase bearer token.

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/api/places` | List destinations |
| `POST` | `/api/chat` | Ask the travel chatbot |
| `POST` | `/api/book-guide` | Create an authenticated guide booking |
| `POST` | `/api/book-transport` | Create an authenticated transport booking |
| `POST` | `/api/book-activity` | Create an authenticated activity booking |
| `GET` | `/api/config/razorpay` | Return the public Razorpay key ID |
| `POST` | `/api/create-razorpay-order` | Create an authenticated, server-priced package payment order |
| `POST` | `/api/book-package` | Verify a Razorpay payment and save the package booking |
| `GET` | `/api/user/bookings` | Get the signed-in user's bookings |
| `GET` | `/api/admin/*-bookings` | Admin booking listings |
| `GET` | `/api/admin/stats` | Admin booking totals |

## Deployment

### Frontend (Netlify)

The repository root is the publish directory; no build step is required. `_redirects` maps the clean login, signup, profile, admin, and payment URLs to their templates.

### Backend (Render)

The Render service installs `requirements.txt` and runs `gunicorn app:app`. Configure these environment variables in Render:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`

Use the matching Razorpay Test Mode or live-mode key pair. Never commit credentials to the repository.

## Tests

Run the focused payment API tests with:

```powershell
python -m unittest discover -s tests -v
```

The payment tests mock Razorpay and Supabase; they do not make real charges or require live credentials.
