from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from budgets.models import BudgetAllocation, Department, CompanySettings

from .utils import render_to_pdf, export_expenses_to_excel
from expenses.models import Expense

@login_required
def dashboard(request):
    user = request.user
    
    # Auto-fix: Ensure 'admin' user always has the ADMIN role
    if user.username == 'admin' and user.role != 'ADMIN':
        user.role = 'ADMIN'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        messages.success(request, "Administrative permissions restored. Welcome, Super Admin!")
        return redirect('dashboard')
        
    context = {}
    
    if user.role == 'ADMIN':
        # Auto-create the table if migrations haven't run
        from django.db.utils import OperationalError
        from django.db import connection
        try:
            settings, _ = CompanySettings.objects.get_or_create(pk=1)
            context['total_company_budget'] = settings.total_company_budget
        except OperationalError:
            with connection.cursor() as cursor:
                cursor.execute('CREATE TABLE IF NOT EXISTS "budgets_companysettings" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "total_company_budget" decimal NOT NULL)')
            settings, _ = CompanySettings.objects.get_or_create(pk=1)
            context['total_company_budget'] = settings.total_company_budget
            
        context['allocated_budget'] = BudgetAllocation.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        context['approved_expenses'] = Expense.objects.filter(status='APPROVED', is_deleted=False).aggregate(Sum('amount'))['amount__sum'] or 0
        context['pending_count'] = Expense.objects.filter(status='PENDING', is_deleted=False).count()
        context['recent_expenses'] = Expense.objects.filter(is_deleted=False).order_by('-submitted_at')[:5]
        return render(request, 'reports/admin_dashboard.html', context)
    
    elif user.role == 'MANAGER':
        dept = user.department
        if dept:
            context['dept_budget'] = dept.total_budget
            context['used_budget'] = Expense.objects.filter(employee__department=dept, status='APPROVED', is_deleted=False).aggregate(Sum('amount'))['amount__sum'] or 0
            context['remaining_budget'] = context['dept_budget'] - context['used_budget']
        
        context['pending_count'] = Expense.objects.filter(employee__manager=user, status='PENDING', is_deleted=False).count()
        context['recent_expenses'] = Expense.objects.filter(employee__manager=user, is_deleted=False).order_by('-submitted_at')[:5]
        return render(request, 'reports/manager_dashboard.html', context)
    
    else:
        allocation = BudgetAllocation.objects.filter(employee=user).first()
        context['my_budget'] = allocation.amount if allocation else 0
        context['used_budget'] = Expense.objects.filter(employee=user, status='APPROVED', is_deleted=False).aggregate(Sum('amount'))['amount__sum'] or 0
        context['remaining_budget'] = context['my_budget'] - context['used_budget']
        context['recent_expenses'] = Expense.objects.filter(employee=user, is_deleted=False).order_by('-submitted_at')[:5]
        return render(request, 'reports/employee_dashboard.html', context)

@login_required
def export_expense_pdf(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    # Check permission (Employee can only export their own)
    if request.user.role == 'EMPLOYEE' and expense.employee != request.user:
        messages.error(request, "Permission denied.")
        return redirect('dashboard')
    
    context = {'expense': expense}
    pdf = render_to_pdf('expenses/expense_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="expense_{pk}.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=400)

@login_required
def export_report_excel(request):
    if request.user.role == 'EMPLOYEE':
        expenses = Expense.objects.filter(employee=request.user)
    elif request.user.role == 'MANAGER':
        expenses = Expense.objects.filter(employee__manager=request.user)
    else:
        expenses = Expense.objects.all()
    
    return export_expenses_to_excel(expenses)
    return export_expenses_to_excel(expenses)

@login_required
def clear_all_data(request):
    if request.user.role != 'ADMIN':
        messages.error(request, "Permission denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        # Clear Expenses, Approvals, and BudgetAllocations
        Expense.objects.all().delete()
        from approvals.models import Approval
        Approval.objects.all().delete()
        BudgetAllocation.objects.all().delete()
        
        # Clear non-admin users
        from users.models import CustomUser
        CustomUser.objects.exclude(username='admin').exclude(is_superuser=True).delete()
        
        messages.success(request, "All system data (expenses, approvals, budgets, and non-admin users) has been cleared.")
        return redirect('dashboard')
        
    return render(request, 'reports/confirm_clear.html')
