from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense, ExpenseCategory
from .forms import ExpenseForm
from django.contrib import messages

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(employee=request.user, is_deleted=False).order_by('-submitted_at')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def submit_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.employee = request.user
            expense.save()
            messages.success(request, "Expense submitted successfully and is pending approval.")
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/submit_expense.html', {'form': form})

@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    
    # Permission check
    user = request.user
    if user.role == 'ADMIN':
        pass # Admin can see everything
    elif user.role == 'MANAGER':
        if expense.employee != user and expense.employee.manager != user:
            messages.error(request, "Permission denied.")
            return redirect('dashboard')
    else: # Employee
        if expense.employee != user:
            messages.error(request, "Permission denied.")
            return redirect('dashboard')
            
    return render(request, 'expenses/expense_detail.html', {'expense': expense})
