import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='ADMIN')
    print('Superuser "admin" created with ADMIN role.')
else:
    u = User.objects.get(username='admin')
    u.role = 'ADMIN'
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print('Updated existing user "admin" to ADMIN role.')
