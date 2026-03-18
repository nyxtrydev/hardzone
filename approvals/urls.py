from django.urls import path
from . import views

urlpatterns = [
    path('', views.approval_list, name='approval_list'),
    path('approve/<int:pk>/', views.approve_expense, name='approve_expense'),
    path('reject/<int:pk>/', views.reject_expense, name='reject_expense'),
]
