# Website Documentation

## Important

- Where do I need to change Paths and insert images/files etc?
  - There are TODOS for all the places that need to be changed. Your IDE should be able to find all TODOS.
- What settings.py should I use?
  - Use the current settings.py as the dev settings, while settings_prod.py is for prodction
  - When going in production change name of settings.py -> settings_local.py and settings_prod.py -> settings.py
  - Only the file named "settings.py" is used as the settings
- Where do I get environment variables?
  - Use a .env file to save your variables
  - The file should be located in "project_head"

## Structure
#### Accounts 
- Contains templates and views for user related activities:
  - Registration
  - Profile deletion
  - Password reset
  - View profile 
  - Delete Profile
  
#### Admin Data
- Contains templates and views for entering and managing data used to fill website and other data from backend:
  - List all users
  - Approval mail after approving a new user
  - Changing user status (approving new user)
  - CV data
  - Personal Info data
  - Add, Change or remove data and some utility functions:
    - Education
    - Extracurriculars
    - IT Skills
    - Certificates
    - Work
    - Skills
  
#### Frontend Pages
- Templates and views to render frontend templates:
  - Render:
    - About
    - Landing Page
    - Await admin (await approval for new user)
    - Cookie policy
    - Privacy Policy
    - Terms and Conditions
    - Resume
    - Contact request
  

#### Main App
- Holds base html templates:
  - Navbar
  - Error Page
  - messages (e.g. login successful...)
  - Base template (header logo etc.)
  

#### Project Head
- Holds configurations:
  - Settings 
  - main urls
  
#### User register
- Holds only templates and views for registration
  
## Dev deployment (With current settings.py)
1. Create vitual environment: python -m venv ./venv
2. Install requirements: pip install -r requirements.txt
3. Make migrations: python manage.py makemigrations
4. Migrate: python manage.py migrate
5. Create superuser: python manage.py createsuperuser
6. Run dev Server: python manage.py runserver

## Deploy in Production for Digitalocean 
- (Change settings_prod.py -> settings.py and remove dev settings!)
- Generally Follow: [This Guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)
1. Create vitual environment: python -m venv ./venv
2. Install Requirements
3. Ensure settings.py is correct
4. Setup Django (makemigrations, migrate, createsuperuser)
5. Setup Postgres (follow guide in link above)
6. DJango collectstatic to gather static files in directory
7. Setup gunicorn and nginx conf. See the documentation files for templates
8. Setup SSL/TLS Certificate with lets-encrypt: [Guide](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/)


- Note:
  - gunicorn.sock is in /run/gunicorn.sock directory not in project directory (guide is wrong)



## Email templates

| Email Template  | Description  | Location   | Trigger   |
|---|---|---|---|
|  contact_admin.txt | A user has contacted through the contact form  | accounts  | frontend_pages\views.py  |   
|  contact_user.txt | A user receives confirmation after contact request  | accounts  | frontend_pages\views.py  |   
|  deletion_mail.txt | A user has contacted through the contact form  |  accounts | accounts\views.py  |   
|  password_reset_email.txt |  A user has contacted through the contact form | accounts  | accounts\views.py |
| approval_mail.txt | A user has been approved for access | admin_data | admin_data\views.py |

