from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Approval
from expenses.models import Expense
from django.contrib import messages

@login_required
def approval_list(request):
    if request.user.role == 'EMPLOYEE':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')
    
    if request.user.role == 'ADMIN':
        pending_expenses = Expense.objects.filter(status='PENDING', is_deleted=False)
    else:
        pending_expenses = Expense.objects.filter(status='PENDING', employee__manager=request.user, is_deleted=False)
        
    return render(request, 'approvals/approval_list.html', {'pending_expenses': pending_expenses})

@login_required
def approve_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    user = request.user
    
    if user.role == 'EMPLOYEE':
        messages.error(request, "Permission denied.")
        return redirect('dashboard')
    
    if user.role == 'MANAGER' and expense.employee.manager != user:
        messages.error(request, "This expense is not in your approval queue.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        remarks = request.POST.get('remarks', '')
        Approval.objects.create(
            expense=expense,
            approver=user,
            status='APPROVED',
            remarks=remarks
        )
        expense.status = 'APPROVED'
        expense.save()
        messages.success(request, f"Expense {expense.id} has been approved.")
        return redirect('approval_list')
    return render(request, 'approvals/approve_reject.html', {'expense': expense, 'action': 'Approve'})

@login_required
def reject_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    user = request.user
    
    if user.role == 'EMPLOYEE':
        messages.error(request, "Permission denied.")
        return redirect('dashboard')
        
    if user.role == 'MANAGER' and expense.employee.manager != user:
        messages.error(request, "This expense is not in your approval queue.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        remarks = request.POST.get('remarks', '')
        Approval.objects.create(
            expense=expense,
            approver=user,
            status='REJECTED',
            remarks=remarks
        )
        expense.status = 'REJECTED'
        expense.save()
        messages.warning(request, f"Expense {expense.id} has been rejected.")
        return redirect('approval_list')
    return render(request, 'approvals/approve_reject.html', {'expense': expense, 'action': 'Reject'})
