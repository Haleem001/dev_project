"""
WSGI config for dev_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import cloudinary
from dotenv import load_dotenv
load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev_project.settings')
app = get_wsgi_application()


cloudinary.config( cloud_name= os.getenv("CLOUD_NAME"), 
                   api_key=os.getenv("CLOUDINARY_API_KEY"),
                    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
                    secure=True )


