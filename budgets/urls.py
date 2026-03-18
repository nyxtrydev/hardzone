from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_list, name='budget_list'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/edit/<int:pk>/', views.department_edit, name='department_edit'),
    path('departments/delete/<int:pk>/', views.department_delete, name='department_delete'),
    path('allocate/', views.budget_create, name='budget_create'),
    path('edit/<int:pk>/', views.budget_edit, name='budget_edit'),
    path('delete/<int:pk>/', views.budget_delete, name='budget_delete'),
    path('settings/', views.company_settings, name='company_settings'),
]
