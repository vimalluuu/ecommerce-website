# ARCFORM — Premium Streetwear E-Commerce Platform

> A luxury fashion e-commerce platform built with **Django REST Framework** (backend) and **pure HTML/CSS/JS** (frontend), powered by **Supabase** (PostgreSQL).

---

## ✨ Features

- 🔐 **JWT Authentication** — Secure login / register with token-based sessions
- 🛍️ **Product Catalogue** — Full browse, search, filter, and sort by category / price / tag
- 🧾 **Order Management** — Place, track, and view order history
- ❤️ **Wishlist** — Save items for later, synced per user account
- 🎟️ **Coupon System** — Percentage or fixed discount codes with expiry and usage limits
- 📦 **Admin Dashboard** — Manage products, orders, users, and coupons via Django admin
- 🗺️ **Address Book** — Multiple shipping addresses with default selection
- ⭐ **Reviews & Ratings** — One review per user per product (1-5 stars)
- 💳 **Checkout Flow** — Cart → Address → Coupon → Confirm → Payment
- 📱 **Fully Responsive** — Mobile-first design, works on all screen sizes
- ⚡ **Performance Indexes** — Carefully tuned PostgreSQL indexes for fast queries
- 🔒 **Row Level Security** — Supabase RLS policies so users only access their own data

---

## 🛠 Tech Stack

| Layer       | Technology                              |
|-------------|------------------------------------------|
| **Frontend**  | HTML5, CSS3 (Vanilla), JavaScript (ES6+) |
| **Backend**   | Python 3.11+, Django 5, Django REST Framework |
| **Database**  | PostgreSQL 15 via Supabase               |
| **Auth**      | Django JWT (`djangorestframework-simplejwt`) |
| **Storage**   | Supabase Storage (product images)        |
| **Hosting**   | Railway / Render (backend), Vercel / Netlify (frontend) |

---

## 📁 Project Structure

```
ecommerce website/
├── backend/
│   ├── arcform/                  # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/                    # Auth, profile, addresses
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── products/                 # Products, categories, reviews
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── orders/                   # Orders, order items, coupons
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── wishlist/                 # Wishlist app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html                # Homepage / hero
│   ├── shop.html                 # Product catalogue
│   ├── product.html              # Product detail page
│   ├── cart.html                 # Shopping cart
│   ├── checkout.html             # Checkout flow
│   ├── account.html              # User profile & orders
│   ├── wishlist.html             # Saved items
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── css/
│   │   ├── main.css              # Global design system & tokens
│   │   ├── components.css        # Reusable UI components
│   │   └── pages/               # Page-specific styles
│   └── js/
│       ├── api.js                # Axios/fetch wrapper for backend
│       ├── auth.js               # Token management & auth helpers
│       ├── cart.js               # Cart state & operations
│       └── utils.js              # Shared utilities
├── supabase/
│   └── schema.sql                # Full DB schema with RLS & seed data
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python **3.11+** and `pip`
- A free [Supabase](https://supabase.com) account

---

### 1. Supabase Setup

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Navigate to **SQL Editor** and paste / run the contents of [`supabase/schema.sql`](supabase/schema.sql)
3. Go to **Project Settings → Database** and copy your connection string
4. Go to **Project Settings → API** and copy your `anon` public key and `service_role` key

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# → Open .env and fill in your Supabase credentials (see table below)

# Run migrations & create superuser
python manage.py migrate
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

---

### 3. Frontend Setup

Open `frontend/index.html` directly in your browser, or use the
[VS Code Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension for hot-reload.

The frontend reads `js/api.js` for the base URL — by default it points to `http://localhost:8000`.

---

## 🔌 API Documentation

### Auth

| Method | Endpoint                   | Description                    | Auth Required |
|--------|----------------------------|--------------------------------|---------------|
| POST   | `/api/auth/register/`      | Register new user              | No            |
| POST   | `/api/auth/login/`         | Login → returns JWT tokens     | No            |
| POST   | `/api/auth/token/refresh/` | Refresh access token           | No            |
| GET    | `/api/auth/me/`            | Get current user profile       | ✅ Yes        |
| PATCH  | `/api/auth/me/`            | Update profile                 | ✅ Yes        |

### Products

| Method | Endpoint                      | Description                                       | Auth Required |
|--------|-------------------------------|---------------------------------------------------|---------------|
| GET    | `/api/products/`              | List all active products (filter/search/sort)     | No            |
| GET    | `/api/products/{slug}/`       | Get single product detail                         | No            |
| GET    | `/api/products/featured/`     | List featured products                            | No            |
| GET    | `/api/categories/`            | List all categories                               | No            |
| GET    | `/api/categories/{slug}/`     | Get category + its products                       | No            |

### Reviews

| Method | Endpoint                              | Description              | Auth Required |
|--------|---------------------------------------|--------------------------|---------------|
| GET    | `/api/products/{slug}/reviews/`       | List reviews for product | No            |
| POST   | `/api/products/{slug}/reviews/`       | Submit a review          | ✅ Yes        |

### Wishlist

| Method | Endpoint                        | Description               | Auth Required |
|--------|---------------------------------|---------------------------|---------------|
| GET    | `/api/wishlist/`                | Get user's wishlist       | ✅ Yes        |
| POST   | `/api/wishlist/`                | Add product to wishlist   | ✅ Yes        |
| DELETE | `/api/wishlist/{product_id}/`   | Remove from wishlist      | ✅ Yes        |

### Orders

| Method | Endpoint                   | Description              | Auth Required |
|--------|----------------------------|--------------------------|---------------|
| GET    | `/api/orders/`             | List user's orders       | ✅ Yes        |
| POST   | `/api/orders/`             | Place a new order        | ✅ Yes        |
| GET    | `/api/orders/{id}/`        | Order detail             | ✅ Yes        |

### Coupons

| Method | Endpoint                        | Description          | Auth Required |
|--------|---------------------------------|----------------------|---------------|
| POST   | `/api/coupons/validate/`        | Validate coupon code | ✅ Yes        |

### Addresses

| Method | Endpoint                    | Description               | Auth Required |
|--------|-----------------------------|---------------------------|---------------|
| GET    | `/api/addresses/`           | List user's addresses     | ✅ Yes        |
| POST   | `/api/addresses/`           | Add new address           | ✅ Yes        |
| PATCH  | `/api/addresses/{id}/`      | Update address            | ✅ Yes        |
| DELETE | `/api/addresses/{id}/`      | Delete address            | ✅ Yes        |

---

## 🔑 Environment Variables

Create `backend/.env` from `backend/.env.example`:

| Variable                  | Description                                      | Example                               |
|---------------------------|--------------------------------------------------|---------------------------------------|
| `SECRET_KEY`              | Django secret key (generate with `django-admin`) | `django-insecure-...`                 |
| `DEBUG`                   | Debug mode (`True` in dev, `False` in prod)      | `True`                                |
| `ALLOWED_HOSTS`           | Comma-separated allowed hosts                    | `localhost,127.0.0.1`                 |
| `DATABASE_URL`            | Supabase PostgreSQL connection string            | `postgresql://postgres:...@db.*.supabase.co:5432/postgres` |
| `SUPABASE_URL`            | Your Supabase project URL                        | `https://xxxx.supabase.co`            |
| `SUPABASE_ANON_KEY`       | Supabase `anon` public key                       | `eyJhbG...`                           |
| `SUPABASE_SERVICE_KEY`    | Supabase `service_role` key (keep secret!)       | `eyJhbG...`                           |
| `CORS_ALLOWED_ORIGINS`    | Frontend origins allowed to call the API         | `http://localhost:5500`               |
| `ACCESS_TOKEN_LIFETIME`   | JWT access token lifetime (minutes)              | `60`                                  |
| `REFRESH_TOKEN_LIFETIME`  | JWT refresh token lifetime (days)                | `7`                                   |

---

## 📄 Pages

| Page           | Path                       | Description                             |
|----------------|----------------------------|-----------------------------------------|
| Homepage       | `frontend/index.html`      | Hero, featured products, brand story    |
| Shop           | `frontend/shop.html`       | Full catalogue with filters & search    |
| Product Detail | `frontend/product.html`    | Images, size picker, add to cart        |
| Cart           | `frontend/cart.html`       | Cart items, totals, proceed to checkout |
| Checkout       | `frontend/checkout.html`   | Address, coupon, order confirmation     |
| Login          | `frontend/auth/login.html` | JWT login form                          |
| Register       | `frontend/auth/register.html` | Account creation form                |
| Account        | `frontend/account.html`    | Profile, order history, addresses       |
| Wishlist       | `frontend/wishlist.html`   | Saved products                          |

---

## 🤝 Contributing

Pull requests are welcome. Please:

1. Fork the repo and create a feature branch: `git checkout -b feature/your-feature`
2. Follow existing code style (PEP 8 for Python, BEM-ish naming for CSS)
3. Write clear commit messages
4. Open a PR with a description of changes

---

## 📜 License

**MIT License** — © 2025 ARCFORM. See [LICENSE](LICENSE) for details.
