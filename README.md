# Nightforge - Dark Fantasy Gothic Clothing Shop

## Description
Nightforge - is a full-stack e-commerce web application build with Django
It allows users to browse a catalog of dark fantasy clothing, add products 
to a shopping cart, and securely place orders online with payment integration.

## Features
 - Custom user authentication(login, register, logout, profile management)
 - Product catalog with search, filtering and sorting 
 - Shopping cart system
 - Order creation and management
 - Stripe payment integration (with webhook handling)
 - Email notification after successful orders
 - Image storage using Cloudinary

## Tech Stack
- Backend: Django, Python
- Database: PostgreSQL
- Frontend: HTML, CSS (Tailwind CSS)
- Payments: Stripe
- Media storage: Cloudinary
- Email: Resend / SMTP
- Deployment: Render

## Live Demo on Render
https://nightforge.onrender.com/

## Installation

### 1. Clone the repository
git clone <repo_url>
cd <project-folder>

### 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Setup environment variables

Create '.env' and add:

SC_KEY = your_secret_key
DEBUG = True or False

DB_NAME = your_postgresql_db_name
DB_USER = your_postgresql_user
PASSWORD = your_db_password
DB_HOST = your_db_host
DB_PORT = your_db_port

STRIPE_API_KEY = your_stripe_api_key
STRIPE_WEBHOOK = your_stripe_webhook

EMAIL_HOST_USER = your_gmail
EMAIL_HOST_PASSWORD = your_gmail_app_password

CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret

RESEND_API_KEY = your_resend_api_key

# Optionl
DJANGO_LOG_LEVEL = your_log_level

### 5. Apply migrations
python manage.py makemigrations
python manage.py migrate

### 6. Collect static files
python manage.py collectstatic

### 7. Run server
python manage.py runserver
