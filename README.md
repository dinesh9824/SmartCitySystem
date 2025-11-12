# Smart City System

A Django-based complaint management system for citizens to submit and track city service complaints.

## Features

- **User Authentication**: Registration, login, and logout functionality
- **Citizen Dashboard**: Submit, view, edit, and delete complaints
- **Admin Dashboard**: Manage all complaints and update status
- **Email Notifications**: Automatic email notifications when complaint status changes
- **Responsive Design**: Bootstrap 5 templates for all devices
- **Category System**: Organize complaints by type (Water, Waste, Electricity, Roads, Others)
- **Status Tracking**: Track complaint progress (Pending, In Progress, Resolved)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Environment Setup

#### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install Django
pip install django
```

#### macOS/Linux
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Django
pip install django
```

### Project Setup

1. **Navigate to the project directory:**
   ```bash
   cd SmartCitySystem
   ```

2. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```
   - Username: admin
   - Password: admin123

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:8000/
   ```

## Project Structure

```
SmartCitySystem/
├── SmartCitySystem/
│   ├── __init__.py
│   ├── settings.py          # Django settings with SQLite and email config
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── complaints/
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration with signals
│   ├── forms.py             # Django forms for registration and complaints
│   ├── models.py            # Complaint model
│   ├── signals.py           # Email notification signals
│   ├── urls.py              # App URL patterns
│   └── views.py             # View functions
├── templates/
│   ├── base.html            # Base template with Bootstrap 5
│   ├── home.html            # Welcome page
│   ├── register.html        # User registration
│   ├── login.html           # User login
│   ├── citizen_dashboard.html    # Citizen complaint dashboard
│   ├── add_complaint.html        # Complaint submission form
│   ├── edit_complaint.html       # Edit complaint form
│   ├── delete_complaint.html     # Delete complaint confirmation
│   ├── admin_dashboard.html      # Admin complaint management
│   ├── admin_edit_complaint.html # Admin edit complaint form
│   └── admin_delete_complaint.html # Admin delete complaint confirmation
├── db.sqlite3               # SQLite database
└── manage.py
```

## Usage Guide

### For Citizens

1. **Register**: Create a new account with your details
2. **Login**: Access your dashboard
3. **Submit Complaint**: Fill out the complaint form with:
   - Title
   - Category (Water, Waste, Electricity, Roads, Others)
   - Detailed description
4. **Track Progress**: View your complaints and their status
5. **Edit/Delete**: Modify or remove your complaints

### For Administrators

1. **Login**: Use admin credentials
2. **Access Admin Panel**: View all complaints from all users
3. **Update Status**: Change complaint status (triggers email notification)
4. **Manage Complaints**: Edit or delete any complaint

## Email Notifications

The system sends automatic email notifications when:
- A new complaint is submitted
- Complaint status is updated by admin

Email notifications are configured to use console backend for testing. Check the console output to see email content.

## Database

- **Database**: SQLite (default Django database)
- **Location**: `db.sqlite3` in project root
- **No external database setup required**

## Testing the System

1. **Register a new user account**
2. **Submit a test complaint**
3. **Login as admin** (username: admin, password: admin123)
4. **Update complaint status** to see email notification
5. **Check console output** for email notifications

## Key Features Implemented

✅ User Authentication (Register, Login, Logout)  
✅ Citizen Dashboard with complaint management  
✅ Admin Dashboard for complaint oversight  
✅ Email notification system  
✅ Bootstrap 5 responsive design  
✅ SQLite database (no external setup)  
✅ Complaint categories and status tracking  
✅ Form validation and error handling  
✅ Security (user can only edit own complaints)  

## Commands Reference

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install Django
pip install django

# Create Django project
django-admin startproject SmartCitySystem

# Create Django app
python manage.py startapp complaints

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Troubleshooting

- **Port already in use**: Use `python manage.py runserver 8001` to use a different port
- **Database errors**: Delete `db.sqlite3` and run migrations again
- **Template not found**: Ensure templates are in the `templates/` directory
- **Static files not loading**: Check that Bootstrap CDN links are accessible

## Deployment on Render

### Prerequisites
- A GitHub account
- A Render account (free tier available)

### Deployment Steps

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create a new Web Service on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure the service:**
   - **Name**: smart-city-system (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn SmartCitySystem.wsgi:application`
   - **Root Directory**: `SmartCitySystem` (if your project is in a subdirectory)

4. **Add Environment Variables:**
   Click "Add Environment Variable" and add:
   - `SECRET_KEY`: Generate a new secret key (you can use Django's `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com` (Render will provide this)
   - `DATABASE_URL`: (Automatically provided by Render if you add a PostgreSQL database)

5. **Add PostgreSQL Database (Optional but Recommended):**
   - In Render Dashboard, click "New +" → "PostgreSQL"
   - Create a new database
   - Render will automatically provide the `DATABASE_URL` environment variable
   - The app will automatically use PostgreSQL if `DATABASE_URL` is set

6. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - The first deployment may take a few minutes

### Post-Deployment

1. **Run migrations on Render:**
   - Go to your service → "Shell" tab
   - Run: `python manage.py migrate`

2. **Create superuser:**
   - In the Shell tab, run: `python manage.py createsuperuser`
   - Follow the prompts to create an admin account

3. **Access your application:**
   - Your app will be available at `https://your-app-name.onrender.com`

### Important Notes

- **Static Files**: WhiteNoise is configured to serve static files automatically
- **Database**: The app uses SQLite locally and PostgreSQL on Render
- **Environment Variables**: Never commit `.env` file to Git
- **Secret Key**: Always use a strong, unique secret key in production
- **Debug Mode**: Keep `DEBUG=False` in production for security

### Troubleshooting Deployment

- **Build fails**: Check the build logs in Render dashboard
- **Static files not loading**: Ensure `STATIC_ROOT` is set and `collectstatic` runs during build
- **Database errors**: Verify `DATABASE_URL` is set correctly
- **500 errors**: Check Render logs and ensure all environment variables are set

## Support

For issues or questions, check the Django documentation or contact the development team.
