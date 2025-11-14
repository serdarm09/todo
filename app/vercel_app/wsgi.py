import os
import sys
from django.core.wsgi import get_wsgi_application

# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'app'))

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()

# Vercel serverless function
def handler(request, context):
    return application(request, context)