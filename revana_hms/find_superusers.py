
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

superusers = User.objects.filter(is_superuser=True)

if superusers.exists():
    print("Found Superusers:")
    for u in superusers:
        print(f"Email: {u.email}, Username: {u.username}")
else:
    print("No superusers found.")
