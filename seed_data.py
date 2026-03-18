import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

from expenses.models import ExpenseCategory
from budgets.models import Department
from users.models import CustomUser

def init_data():
    # Categories
    categories = ['Travel', 'Food', 'Office Supplies', 'Client Meeting', 'Fuel', 'Miscellaneous']
    for cat_name in categories:
        ExpenseCategory.objects.get_or_create(name=cat_name)
    print("Categories initialized.")

    # Departments
    depts = ['Operations', 'Marketing', 'Sales', 'HR']
    for dept_name in depts:
        Department.objects.get_or_create(name=dept_name, defaults={'total_budget': 100000})
    print("Departments initialized.")

    # Users
    admin = CustomUser.objects.filter(role='ADMIN').first()
    hr_dept = Department.objects.get(name='HR')
    
    manager, created = CustomUser.objects.get_or_create(
        username='manager',
        defaults={
            'email': 'manager@example.com',
            'role': 'MANAGER',
            'department': hr_dept,
            'is_staff': True
        }
    )
    if created:
        manager.set_password('manager123')
        manager.save()
    
    employee, created = CustomUser.objects.get_or_create(
        username='employee',
        defaults={
            'email': 'employee@example.com',
            'role': 'EMPLOYEE',
            'department': hr_dept,
            'manager': manager
        }
    )
    if created:
        employee.set_password('employee123')
        employee.save()
    
    print("Test users (manager/employee) initialized.")

if __name__ == '__main__':
    init_data()
