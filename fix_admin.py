import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

from users.models import CustomUser

def log(msg):
    print(msg)
    with open('admin_fix_log.txt', 'a') as f:
        f.write(msg + '\n')

try:
    u = CustomUser.objects.get(username='admin')
    u.role = 'ADMIN'
    u.is_staff = True
    u.is_superuser = True
    u.save()
    log(f"SUCCESS: User '{u.username}' updated to role: {u.role} ({u.get_role_display()})")
    
    # Verify
    u_updated = CustomUser.objects.get(username='admin')
    log(f"VERIFICATION: Current role in DB: {u_updated.role}")
except CustomUser.DoesNotExist:
    log("ERROR: User 'admin' does not exist.")
except Exception as e:
    log(f"ERROR: {str(e)}")
