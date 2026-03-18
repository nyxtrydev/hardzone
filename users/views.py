from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'department', 'manager')

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'department', 'manager', 'is_active')

def admin_required(function):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'ADMIN')(function)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@admin_required
def user_list(request):
    users = CustomUser.objects.all().order_by('username')
    return render(request, 'users/user_list.html', {'users': users})

@admin_required
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Create'})

@admin_required
def user_edit(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user_obj.username} updated successfully.")
            return redirect('user_list')
    else:
        form = CustomUserUpdateForm(instance=user_obj)
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Edit', 'user_obj': user_obj})

@admin_required
def user_delete(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)
    if user_obj == request.user:
        messages.error(request, "You cannot delete yourself.")
        return redirect('user_list')
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, f"User {user_obj.username} deleted successfully.")
        return redirect('user_list')
    return render(request, 'users/confirm_delete.html', {'object': user_obj, 'type': 'User', 'cancel_url': 'user_list'})
