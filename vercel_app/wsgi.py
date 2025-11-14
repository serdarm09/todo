import os
import sys

# Proje dizinini Python path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Django ayarlarını set et
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Django'yu başlat
import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()