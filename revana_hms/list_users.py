import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from accounts.models import User

print(f"\n--- Registered Users ---")
print(f"{'ID':<5} {'Email':<30} {'Role':<15} {'Joined'}")
print("-" * 70)

for u in User.objects.all().order_by('id'):
    joined = u.date_joined.strftime('%Y-%m-%d') if u.date_joined else 'N/A'
    print(f"{u.id:<5} {u.email:<30} {u.role:<15} {joined}")
    
print("-" * 70)
print(f"Total: {User.objects.count()}")
