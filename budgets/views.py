from django.shortcuts import render, redirect, get_object_or_404
from .models import Department, BudgetAllocation, CompanySettings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django import forms

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'total_budget']

class BudgetAllocationForm(forms.ModelForm):
    class Meta:
        model = BudgetAllocation
        fields = ['department', 'employee', 'amount', 'start_date', 'end_date', 'notes']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = ['total_company_budget']

def admin_required(function):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'ADMIN')(function)

@login_required
def budget_list(request):
    user = request.user
    if user.role == 'ADMIN':
        allocations = BudgetAllocation.objects.all()
    elif user.role == 'MANAGER':
        allocations = BudgetAllocation.objects.filter(department=user.department)
    else:
        allocations = BudgetAllocation.objects.filter(employee=user)
    
    return render(request, 'budgets/budget_list.html', {'allocations': allocations})

@admin_required
def department_list(request):
    departments = Department.objects.all().order_by('name')
    return render(request, 'budgets/department_list.html', {'departments': departments})

@admin_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully.")
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'budgets/department_form.html', {'form': form, 'action': 'Create'})

@admin_required
def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f"Department {dept.name} updated successfully.")
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'budgets/department_form.html', {'form': form, 'action': 'Edit', 'dept': dept})

@admin_required
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, f"Department {dept.name} deleted successfully.")
        return redirect('department_list')
    return render(request, 'budgets/confirm_delete.html', {'object': dept, 'type': 'Department', 'cancel_url': 'department_list'})

@admin_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget allocated successfully.")
            return redirect('budget_list')
    else:
        form = BudgetAllocationForm()
    return render(request, 'budgets/budget_form.html', {'form': form, 'action': 'Allocate'})

@admin_required
def budget_edit(request, pk):
    allocation = get_object_or_404(BudgetAllocation, pk=pk)
    if request.method == 'POST':
        form = BudgetAllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget allocation updated successfully.")
            return redirect('budget_list')
    else:
        form = BudgetAllocationForm(instance=allocation)
    return render(request, 'budgets/budget_form.html', {'form': form, 'action': 'Edit', 'allocation': allocation})

@admin_required
def budget_delete(request, pk):
    allocation = get_object_or_404(BudgetAllocation, pk=pk)
    if request.method == 'POST':
        allocation.delete()
        messages.success(request, "Budget allocation deleted successfully.")
        return redirect('budget_list')
    return render(request, 'budgets/confirm_delete.html', {'object': allocation, 'type': 'Budget Allocation', 'cancel_url': 'budget_list'})
    return render(request, 'budgets/confirm_delete.html', {'object': allocation, 'type': 'Budget Allocation', 'cancel_url': 'budget_list'})

@admin_required
def company_settings(request):
    from django.db.utils import OperationalError
    from django.db import connection
    try:
        settings, created = CompanySettings.objects.get_or_create(pk=1)
    except OperationalError:
        with connection.cursor() as cursor:
            cursor.execute('CREATE TABLE IF NOT EXISTS "budgets_companysettings" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "total_company_budget" decimal NOT NULL)')
        settings, created = CompanySettings.objects.get_or_create(pk=1)
        
    if request.method == 'POST':
        form = CompanySettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Company settings updated successfully.")
            return redirect('dashboard')
    else:
        form = CompanySettingsForm(instance=settings)
    return render(request, 'budgets/company_settings.html', {'form': form})
