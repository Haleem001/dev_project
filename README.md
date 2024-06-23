# IDP App Backend

Welcome to the backend repository for the IDP App built with Django. This repository contains the server-side implementation including API endpoints, database models, and business logic for the IDP app.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Running the Server](#running-the-server)
- [API Documentation](#api-documentation)

## Installation

To get started with the  App backend, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd adoption-app-backend


2. **Create and activate virtual environment:**


# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3. **Install Dependencies**

pip install -r requirements.txt


##  Setup 

1. **Database Setup**
Ensure Database settings is configured in `settings.py` file:
For the database you can uncomment the sqlite settings in the `settings.py` 
and comment the postgresql setting to use sqlite as your database
or do vice versa and setup a .env file and add your postgres credentials to use postgres

# Apply migrations to create database tables:

python manage.py makemigrations
python manage.py migrate

# Create a superuser to access the Django admin interface and API endpoints:
While in the base directory do:
py create_superuser_script.py

The `create_superuser_script.py` can be edited

## Running the Server
# To run the Django development server:
python manage.py runserver

The server will start at ` http://localhost:8000/`.

Go to ` http://localhost:8000/admin` to visit the admin interface.

## API Documentation

To view the API Doc go to:

`http://localhost:8000/api/swagger/`



