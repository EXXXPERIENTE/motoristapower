import os
import django
import sys

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motoristapower.settings')
django.setup()

from django.contrib.auth import get_user_model


def create_superuser():
    User = get_user_model()

    # Deleta usuário admin existente
    User.objects.filter(username='admin').delete()

    # Cria novo superusuário
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='123456'
    )
    print('✅ SUPERUSUÁRIO CRIADO: admin / 123456')
    return user


if __name__ == '__main__':
    create_superuser()