from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('submit/', views.submit_expense, name='submit_expense'),
    path('<int:pk>/', views.expense_detail, name='expense_detail'),
]
