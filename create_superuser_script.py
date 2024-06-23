# import necessary modules
import os
import django

# set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev_project.settings')
django.setup()

# import your custom user model
from django.contrib.auth import get_user_model

# get your custom user model
User = get_user_model()

def create_superuser():
    # Define superuser data
    # 
    superuser_data = {
        'status': 'Admin',  # This defines the status of user
        'username': 'admin', # This is the username 
        'email': 'admin@example.com', #replace it with your email
        'password': 'admin_password',  # change the password to a more secure password
        'first_name': 'Admin',
        'last_name': 'User',
    }

    # Create superuser using custom create_superuser method
    try:
        User.objects.create_superuser(
            superuser_data['status'],
            superuser_data['username'],
            superuser_data['email'],
            superuser_data['password'],
            
            superuser_data['first_name'],
            superuser_data['last_name'],
        )
        print('Superuser created successfully!')
    except Exception as e:
        print(f'Error creating superuser: {str(e)}')

if __name__ == '__main__':
    create_superuser()
