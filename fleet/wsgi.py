import os
from django.core.wsgi import get_wsgi_application

# Aponte para o settings correto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fleet.settings')

# Variável obrigatória que Django precisa
application = get_wsgi_application()
