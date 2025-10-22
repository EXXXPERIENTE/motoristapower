# teste_whatsapp.py
import os
import django
import sys

sys.path.append('C:/APPY/MotoristaPower')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fleet.settings')
django.setup()

from drivers.services_whatsapp import testar_whatsapp

print("🧪 TESTE MANUAL DO WHATSAPP")
print("=" * 50)
testar_whatsapp()