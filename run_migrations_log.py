import subprocess
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    with open('migration_log.txt', 'a') as f:
        f.write(f"COMMAND: {cmd}\n")
        f.write(f"STDOUT:\n{result.stdout}\n")
        f.write(f"STDERR:\n{result.stderr}\n")
        f.write("-" * 40 + "\n")

if os.path.exists('migration_log.txt'):
    os.remove('migration_log.txt')

run_cmd('venv\\Scripts\\python manage.py makemigrations users')
run_cmd('venv\\Scripts\\python manage.py makemigrations budgets')
run_cmd('venv\\Scripts\\python manage.py makemigrations expenses')
run_cmd('venv\\Scripts\\python manage.py makemigrations approvals')
run_cmd('venv\\Scripts\\python manage.py makemigrations reports')
run_cmd('venv\\Scripts\\python manage.py migrate')
