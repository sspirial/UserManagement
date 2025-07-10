User Management System

A django app to help in managing users, groups, and their permissions.

## Features
- User registration and authentication
- Group management
- Permission management
- User profile management
- User verification via email

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sspirial/UserManagement.git
   cd UserManagement
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser 
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
6. Access the admin panel at `http://127.0.0.1:8000/admin/`.
7. Access the user management system at `http://127.0.1:8000/accounts/`.
8. Register a new user and verify via email.
9. Manage users, groups, and permissions through the admin panel.