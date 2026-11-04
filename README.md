# MediShare

Redistribute Unused Medicine — a community-driven medicine donation platform that helps people donate surplus medicines safely and enables verified palliative units to redistribute them to patients and families in need.

Live demo: https://medi-share.onrender.com/

## Overview

MediShare is a Django-based web application designed to reduce medicine waste while improving access to essential healthcare supplies. Donors can submit unused but valid medicines, palliative care units can review and collect those donations, and patients can request available stock from trusted local units.

The platform uses role-based access for donors, palliative units, and administrators, with verification workflows to ensure safe handling and coordination. It combines medicine inventory management, location-aware pickup, and request tracking in a single operational workflow.

## Problem it solves

A significant amount of usable medicine is discarded due to expiry, over-purchasing, or changing treatment plans. At the same time, many patients and families struggle to access affordable or timely medicines. MediShare addresses this by connecting surplus medicine donors with local verified care units that can redistribute the stock safely and sustainably.

## Key features

- Donor registration and profile management
- Medicine donation submission with image upload and expiry tracking
- Map-based pickup location selection using Leaflet + OpenStreetMap
- Nearest verified-unit matching using geospatial distance calculation
- Unit registration and verification workflow for care centers
- Donation review and acceptance by palliative units
- Inventory management for collected medicines
- Patient-side medicine request and status tracking
- Admin dashboard for monitoring users, units, donations, and inventory health
- Search and filtering for available medicines by name

## Tech stack

- Python
- Django 6.0.5
- PostgreSQL (production-ready configuration via dj-database-url)
- Gunicorn
- WhiteNoise for static files
- Bootstrap 5
- Leaflet + OpenStreetMap for location mapping
- Chart.js for dashboard analytics

## Project structure

```text
medishare/
├── manage.py
├── Procfile
├── requirements.txt
├── medishare/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── user/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── utils/
├── unit/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── customadmin/
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── templates/
│   ├── 01-welcome/
│   ├── 02-auth/
│   ├── 03-admin/
│   ├── 04-unit/
│   └── 05-user/
├── static/
│   ├── css/
│   └── js/
└── staticfiles/
```

## Local development setup

### Prerequisites

- Python 3.12+
- pip
- PostgreSQL (optional for local development; SQLite fallback exists in the project config)

### Steps

```bash
cd medishare
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Environment variables

Set the following before deployment or production use:

```bash
export SECRET_KEY="your-secret-key"
export DEBUG="True"
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
```

If `DATABASE_URL` is not set, the project falls back to SQLite in `settings.py` for local testing.

## Roles in the platform

### Donors
- Donate surplus medicines
- Upload medicine images
- Provide expiry data and pickup information
- Track donation status

### Palliative Units
- Register and verify care units
- Review incoming donation requests
- Accept and collect medicines
- Manage inventory
- Approve or reject medicine requests

### Admins
- Verify palliative units
- Monitor platform metrics
- Remove invalid or unsafe donations
- Review inventory and request activity

## Production note

This project is structured for deployment on a Django hosting platform such as Render, Heroku, or a VPS, and includes a `Procfile` for Gunicorn. Before production deployment, it is recommended to:

- rotate and secure any committed database credentials
- configure environment variables properly
- set a strong secret key
- enforce SSL and secure cookies
- validate media uploads and file storage configuration
- add automated tests and CI checks

## License

This project is currently distributed without a formal license file in the repository. Please confirm with the repository owner before using it in commercial or production contexts.

## Demo

https://medi-share.onrender.com/
