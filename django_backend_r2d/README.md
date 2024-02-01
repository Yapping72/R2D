# Generate New Django Secret Key
1. Navigate to directory containing manage.py
2. ``python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'``