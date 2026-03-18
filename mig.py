import os
os.system(r"venv\Scripts\python manage.py makemigrations budgets")
os.system(r"venv\Scripts\python manage.py migrate")
print("Done styling migrations")
