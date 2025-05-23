# Event Management System – Django Backend

This is a powerful backend system for managing events with advanced features like role-based permissions, conflict resolution, and audit trails. Built using Django and Django REST Framework.

---

##  Features

-  User Registration & Authentication (JWT)
-  Role-Based Access Control (Admin, Organizer, Attendee)
-  Event CRUD (Create, Read, Update, Delete)
-  Recurring Events Support
-  Filtering, Searching, and Ordering
-  Event Versioning & Audit Trail
-  Real-time Data Synchronization (optimizable)
-  API-ready for frontend integration
-  Fully Tested & Deployed

---

##  Project Structure
neofi-backend/
├── auth_users/ # Custom User App
├── events/ # Event CRUD + Filtering
├── neofi_backend/ # Main Django Project
├── requirements.txt
├── manage.py
└── README.md

---

##  Setup Locally

1. **Clone the repo**
```bash
git clone https://github.com/your-username/event-management-system.git
cd neofi-backend

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
## Live Deployment
 Hosted on Render
 https://event-management-system-bqt3.onrender.com/
 Testing with Postman
Local base URL: http://127.0.0.1:8000

Live base URL: https://event-management-system-bqt3.onrender.com

You can also set up a Postman Environment:

Create an environment variable base_url

Set its value to the live URL

Use {{base_url}}/api/auth/register/ in your requests

Tech Stack
Python & Django

Django REST Framework

PostgreSQL (Render / ElephantSQL)

Gunicorn (for production)

JWT Authentication

Run Tests
python manage.py test

Author
Made with  by Aditya
Freelance Backend Developer | Django Specialist

GitHub: adityapowar88

License
This project is open-source and available under the MIT License.

Let me know if you'd like to include sample request/response formats or diagrams next.


