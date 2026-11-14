# PlanMyValentine — Full Production Deployment with Caddy Server

> Complete step-by-step guide to deploy this Django app on a Linux VPS with **Caddy** as reverse proxy, **Gunicorn** as WSGI server, and proper static file serving (no CSS/JS errors).

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Server Initial Setup](#2-server-initial-setup)
3. [Clone & Configure the Project](#3-clone--configure-the-project)
4. [Python Virtual Environment & Dependencies](#4-python-virtual-environment--dependencies)
5. [Django Production Settings](#5-django-production-settings)
6. [Collect Static Files](#6-collect-static-files)
7. [Database Setup & Migrations](#7-database-setup--migrations)
8. [Test with Gunicorn](#8-test-with-gunicorn)
9. [Create Gunicorn Systemd Service](#9-create-gunicorn-systemd-service)
10. [Install & Configure Caddy](#10-install--configure-caddy)
11. [Caddyfile — Full Configuration](#11-caddyfile--full-configuration)
12. [Enable & Start Services](#12-enable--start-services)
13. [Firewall Configuration](#13-firewall-configuration)
14. [SSL / HTTPS (Automatic with Caddy)](#14-ssl--https-automatic-with-caddy)
15. [Verify Everything Works](#15-verify-everything-works)
16. [Troubleshooting — CSS / Static Files Not Loading](#16-troubleshooting--css--static-files-not-loading)
17. [Maintenance & Updates](#17-maintenance--updates)
18. [Security Hardening Checklist](#18-security-hardening-checklist)
19. [Full File Reference](#19-full-file-reference)

---

## 1. Prerequisites

| Requirement          | Details                                                |
|----------------------|--------------------------------------------------------|
| **VPS / Server**     | Ubuntu 22.04+ or Debian 12+ (any Linux with systemd)  |
| **Domain Name**      | e.g. `planmyvalentine.in` pointing to your server IP  |
| **Python**           | 3.10+                                                  |
| **Root/Sudo access** | Required for service setup                             |
| **OpenAI API Key**   | For AI plan generation                                 |

### DNS Setup

Point your domain's **A record** to your server's public IP:

```
Type: A
Name: @                (or planmyvalentine.in)
Value: YOUR_SERVER_IP
TTL: 300
```

If you want `www` too:

```
Type: CNAME
Name: www
Value: planmyvalentine.in
TTL: 300
```

---

## 2. Server Initial Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv git curl wget ufw

# Create a dedicated user (recommended)
sudo adduser valentine
sudo usermod -aG sudo valentine

# Switch to that user
su - valentine
```

---

## 3. Clone & Configure the Project

```bash
# Clone your repo (replace with your actual repo URL)
cd /home/valentine
git clone https://github.com/YOUR_USERNAME/Valentine.git
cd Valentine

# Or upload files via SCP/SFTP
# scp -r ./Valentine valentine@YOUR_SERVER_IP:/home/valentine/Valentine
```

### Create the `.env` file

```bash
nano .env
```

Add:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
DJANGO_SECRET_KEY=your-very-long-random-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=planmyvalentine.in,www.planmyvalentine.in
```

Generate a secret key:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 4. Python Virtual Environment & Dependencies

```bash
cd /home/valentine/Valentine

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install production dependencies
pip install gunicorn whitenoise
```

### Updated `requirements.txt` for production

```
Django==4.2.9
openai==0.28.1
python-dotenv==1.0.0
gunicorn==21.1.0
whitenoise==6.6.0
```

---

## 5. Django Production Settings

Edit `planmyvalentine/settings.py` — make these changes for production:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# ============ PRODUCTION SETTINGS ============

# Secret Key — from .env (NEVER hardcode in production)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-insecure-key-change-me')

# Debug — MUST be False in production
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

# Allowed Hosts — from .env
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')

# ============ MIDDLEWARE (add WhiteNoise) ============

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',       # <-- ADD THIS LINE (right after SecurityMiddleware)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============ STATIC FILES (critical for no CSS errors) ============

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'               # <-- ADD THIS LINE

# WhiteNoise storage for compressed + cached static files
STORAGES = {                                           # <-- ADD THIS BLOCK
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ============ SECURITY SETTINGS (production) ============

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = False           # Caddy handles HTTPS, don't redirect internally
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    CSRF_TRUSTED_ORIGINS = [
        'https://planmyvalentine.in',
        'https://www.planmyvalentine.in',
    ]

# ============ LOGGING ============

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django_error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

> **Replace `planmyvalentine.in` everywhere with your actual domain name.**

---

## 6. Collect Static Files

This is the **most critical step** to prevent CSS/JS errors:

```bash
cd /home/valentine/Valentine
source .venv/bin/activate

# Create logs directory
mkdir -p logs

# Collect all static files into STATIC_ROOT (staticfiles/)
python manage.py collectstatic --noinput
```

Expected output:

```
XXX static files copied to '/home/valentine/Valentine/staticfiles'.
```

### Verify static files exist

```bash
ls -la staticfiles/
ls -la staticfiles/css/
ls -la staticfiles/js/

# You should see:
# staticfiles/css/style.css
# staticfiles/css/style.css.gz          (compressed by WhiteNoise)
# staticfiles/js/main.js
# staticfiles/js/main.js.gz            (compressed by WhiteNoise)
```

---

## 7. Database Setup & Migrations

```bash
cd /home/valentine/Valentine
source .venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser for admin panel
python manage.py createsuperuser
```

### File permissions for SQLite

```bash
# The db.sqlite3 file AND its parent directory need write permissions
chmod 664 db.sqlite3
chmod 775 /home/valentine/Valentine
```

> **For high-traffic production**, consider switching to PostgreSQL. SQLite works fine for moderate traffic.

---

## 8. Test with Gunicorn

```bash
cd /home/valentine/Valentine
source .venv/bin/activate

# Test Gunicorn (should start without errors)
gunicorn planmyvalentine.wsgi:application --bind 0.0.0.0:8000 --workers 3

# Visit http://YOUR_SERVER_IP:8000 to verify
# Press Ctrl+C to stop
```

If you see errors, fix them before proceeding.

---

## 9. Create Gunicorn Systemd Service

```bash
sudo nano /etc/systemd/system/valentine.service
```

Paste:

```ini
[Unit]
Description=PlanMyValentine Gunicorn Daemon
After=network.target

[Service]
User=valentine
Group=www-data
WorkingDirectory=/home/valentine/Valentine
EnvironmentFile=/home/valentine/Valentine/.env
ExecStart=/home/valentine/Valentine/.venv/bin/gunicorn \
    planmyvalentine.wsgi:application \
    --bind unix:/home/valentine/Valentine/valentine.sock \
    --workers 3 \
    --timeout 120 \
    --access-logfile /home/valentine/Valentine/logs/gunicorn_access.log \
    --error-logfile /home/valentine/Valentine/logs/gunicorn_error.log \
    --capture-output
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Enable & start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable valentine
sudo systemctl start valentine
sudo systemctl status valentine
```

### Verify the socket was created

```bash
ls -la /home/valentine/Valentine/valentine.sock
# Should show: srwxrwxrwx ... valentine.sock
```

---

## 10. Install & Configure Caddy

### Install Caddy (official method)

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list

sudo apt update
sudo apt install caddy
```

### Verify installation

```bash
caddy version
# Should show: v2.x.x
```

---

## 11. Caddyfile — Full Configuration

```bash
sudo nano /etc/caddy/Caddyfile
```

### Option A: With a Domain Name (recommended — auto HTTPS)

```caddyfile
planmyvalentine.in, www.planmyvalentine.in {
    # Encode responses with gzip/zstd
    encode gzip zstd

    # Serve static files directly from Caddy (fastest, no CSS errors)
    handle_path /static/* {
        root * /home/valentine/Valentine/staticfiles
        file_server
    }

    # Serve media files if you add uploads later
    handle_path /media/* {
        root * /home/valentine/Valentine/media
        file_server
    }

    # Reverse proxy everything else to Gunicorn
    reverse_proxy unix//home/valentine/Valentine/valentine.sock {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }

    # Security headers
    header {
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        Referrer-Policy strict-origin-when-cross-origin
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        -Server
    }

    # Logging
    log {
        output file /var/log/caddy/valentine_access.log {
            roll_size 10mb
            roll_keep 5
        }
    }
}
```

### Option B: Without a Domain (IP only / localhost — no auto HTTPS)

```caddyfile
:80 {
    encode gzip zstd

    handle_path /static/* {
        root * /home/valentine/Valentine/staticfiles
        file_server
    }

    handle_path /media/* {
        root * /home/valentine/Valentine/media
        file_server
    }

    reverse_proxy unix//home/valentine/Valentine/valentine.sock {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }

    log {
        output file /var/log/caddy/valentine_access.log
    }
}
```

### Create log directory

```bash
sudo mkdir -p /var/log/caddy
sudo chown caddy:caddy /var/log/caddy
```

---

## 12. Enable & Start Services

```bash
# Give Caddy user read access to static files and socket
sudo usermod -aG valentine caddy

# Validate Caddyfile syntax
sudo caddy validate --config /etc/caddy/Caddyfile

# Reload/restart Caddy
sudo systemctl restart caddy
sudo systemctl enable caddy
sudo systemctl status caddy

# Verify both services are running
sudo systemctl status valentine     # Gunicorn
sudo systemctl status caddy         # Caddy
```

---

## 13. Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow SSH (don't lock yourself out!)
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

---

## 14. SSL / HTTPS (Automatic with Caddy)

**Caddy automatically provisions and renews SSL certificates from Let's Encrypt** when you use a domain name in the Caddyfile. No extra configuration needed!

Requirements:
- Domain A record points to your server IP
- Ports 80 and 443 are open
- You used a domain name (not IP) in the Caddyfile

Verify:

```bash
# Check certificate
curl -I https://planmyvalentine.in

# Should show:
# HTTP/2 200
# ...
```

---

## 15. Verify Everything Works

### Step-by-step verification

```bash
# 1. Check Gunicorn is running
sudo systemctl status valentine
# Active: active (running)

# 2. Check Caddy is running
sudo systemctl status caddy
# Active: active (running)

# 3. Check the Unix socket exists
ls -la /home/valentine/Valentine/valentine.sock

# 4. Test static files directly
curl -I https://planmyvalentine.in/static/css/style.css
# Should return: HTTP/2 200, content-type: text/css

curl -I https://planmyvalentine.in/static/js/main.js
# Should return: HTTP/2 200, content-type: application/javascript

# 5. Test the main page
curl -s https://planmyvalentine.in | head -50
# Should show HTML with proper content

# 6. Open in browser
# Visit https://planmyvalentine.in
# - Check DevTools (F12) → Console → No 404 errors for CSS/JS
# - Check DevTools → Network → All static files return 200
```

---

## 16. Troubleshooting — CSS / Static Files Not Loading

### Problem: CSS/JS returns 404

**Cause:** Static files not collected or Caddy path mismatch.

```bash
# Fix: Re-collect static files
cd /home/valentine/Valentine
source .venv/bin/activate
python manage.py collectstatic --noinput --clear

# Verify files exist in correct location
ls -la staticfiles/css/style.css
ls -la staticfiles/js/main.js
```

### Problem: Caddy can't read static files (403 Forbidden)

**Cause:** File permission issue.

```bash
# Fix permissions
sudo chown -R valentine:www-data /home/valentine/Valentine/staticfiles
sudo chmod -R 755 /home/valentine/Valentine/staticfiles

# Also ensure Caddy/www-data can traverse to the directory
sudo chmod 755 /home/valentine
sudo chmod 755 /home/valentine/Valentine
```

### Problem: Static files load but CSS looks broken

**Cause:** `STATIC_URL` mismatch between Django and Caddyfile.

```
# In settings.py:
STATIC_URL = '/static/'

# In Caddyfile, the handle_path must strip /static/ prefix:
handle_path /static/* {
    root * /home/valentine/Valentine/staticfiles
    file_server
}
```

The `handle_path` directive **strips the matched prefix** (`/static/`) before looking up files in the root. So a request to `/static/css/style.css` becomes `css/style.css` → served from `staticfiles/css/style.css`. This is correct.

### Problem: Bootstrap/Google Fonts not loading

**Cause:** These are CDN resources (loaded from external URLs). Check:
- Server has internet access
- No Content Security Policy blocking them
- The CDN URLs are correct (they are in `base.html`)

### Problem: 502 Bad Gateway

**Cause:** Gunicorn is down or socket permission issue.

```bash
# Check Gunicorn logs
sudo journalctl -u valentine -n 50
cat /home/valentine/Valentine/logs/gunicorn_error.log

# Restart Gunicorn
sudo systemctl restart valentine

# Check socket permissions
ls -la /home/valentine/Valentine/valentine.sock
```

### Problem: CSRF errors on form submission

**Cause:** Missing `CSRF_TRUSTED_ORIGINS` setting.

```python
# In settings.py, add:
CSRF_TRUSTED_ORIGINS = [
    'https://planmyvalentine.in',
    'https://www.planmyvalentine.in',
]
```

### Problem: Gunicorn won't start — ModuleNotFoundError

```bash
# Make sure you're using the venv Python
/home/valentine/Valentine/.venv/bin/python -c "import django; print(django.get_version())"
# Should print: 4.2.9

# Reinstall dependencies
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 17. Maintenance & Updates

### Deploy code updates

```bash
cd /home/valentine/Valentine
git pull origin main

source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

sudo systemctl restart valentine
# Caddy doesn't need restart for code changes
```

### View logs

```bash
# Gunicorn logs
sudo journalctl -u valentine -f
cat logs/gunicorn_access.log
cat logs/gunicorn_error.log

# Caddy logs
sudo journalctl -u caddy -f
cat /var/log/caddy/valentine_access.log

# Django error logs
cat logs/django_error.log
```

### Backup database

```bash
# SQLite backup
cp /home/valentine/Valentine/db.sqlite3 /home/valentine/backups/db_$(date +%Y%m%d).sqlite3

# Automate with cron
crontab -e
# Add: 0 2 * * * cp /home/valentine/Valentine/db.sqlite3 /home/valentine/backups/db_$(date +\%Y\%m\%d).sqlite3
```

---

## 18. Security Hardening Checklist

- [x] `DEBUG = False` in production
- [x] Strong `SECRET_KEY` from `.env`
- [x] `ALLOWED_HOSTS` set properly
- [x] HTTPS enforced (Caddy auto-SSL)
- [x] CSRF trusted origins configured
- [x] Security headers set in Caddyfile
- [x] HSTS enabled
- [x] `.env` file is NOT in git (add to `.gitignore`)
- [x] Firewall enabled (UFW)
- [x] Gunicorn runs as non-root user
- [x] Database file permissions restricted
- [x] Error logging to file (not console)

### `.gitignore` additions

```
.env
db.sqlite3
staticfiles/
logs/
*.sock
__pycache__/
.venv/
```

---

## 19. Full File Reference

### Project structure on server

```
/home/valentine/Valentine/
├── .env                          # Environment variables (NOT in git)
├── .venv/                        # Python virtual environment
├── manage.py
├── requirements.txt
├── db.sqlite3                    # SQLite database
├── valentine.sock                # Gunicorn Unix socket (auto-created)
├── logs/
│   ├── django_error.log
│   ├── gunicorn_access.log
│   └── gunicorn_error.log
├── static/                       # Source static files (development)
│   ├── css/style.css
│   └── js/main.js
├── staticfiles/                  # Collected static files (production — Caddy serves from here)
│   ├── css/
│   │   ├── style.css
│   │   └── style.*.css           # Hashed by WhiteNoise
│   ├── js/
│   │   ├── main.js
│   │   └── main.*.js
│   └── admin/                    # Django admin static files
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── city.html
│   ├── letter.html
│   ├── planner_form.html
│   ├── result.html
│   └── share.html
├── planmyvalentine/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                         # Core app (home page, cities)
│   ├── views.py
│   ├── urls.py
│   ├── prompts.py                # OpenAI integration + city data
│   └── utils.py
└── planner/                      # Planner app (form, results, sharing)
    ├── views.py
    ├── urls.py
    ├── models.py
    ├── forms.py
    └── admin.py
```

### Systemd services

| File                                     | Purpose               |
|------------------------------------------|------------------------|
| `/etc/systemd/system/valentine.service`  | Gunicorn WSGI server   |
| `/etc/caddy/Caddyfile`                   | Caddy reverse proxy    |

### Key commands cheat sheet

```bash
# Start/Stop/Restart Gunicorn
sudo systemctl start valentine
sudo systemctl stop valentine
sudo systemctl restart valentine

# Start/Stop/Restart Caddy
sudo systemctl start caddy
sudo systemctl stop caddy
sudo systemctl restart caddy
sudo caddy reload --config /etc/caddy/Caddyfile

# Check status
sudo systemctl status valentine
sudo systemctl status caddy

# View live logs
sudo journalctl -u valentine -f
sudo journalctl -u caddy -f

# Django management
cd /home/valentine/Valentine && source .venv/bin/activate
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
```

---

## Quick Deploy Summary (TL;DR)

```bash
# 1. Server setup
sudo apt update && sudo apt install -y python3 python3-venv git curl
sudo apt install caddy

# 2. Project setup
cd /home/valentine/Valentine
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install gunicorn whitenoise
cp .env.example .env && nano .env    # Add keys

# 3. Django production prep
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# 4. Configure services
sudo nano /etc/systemd/system/valentine.service   # Gunicorn
sudo nano /etc/caddy/Caddyfile                     # Caddy

# 5. Start everything
sudo systemctl enable --now valentine
sudo systemctl restart caddy

# 6. Open browser → https://planmyvalentine.in ✅
```

---

*Last updated: February 2026*
