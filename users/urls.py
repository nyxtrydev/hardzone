from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('manage/', views.user_list, name='user_list'),
    path('manage/create/', views.user_create, name='user_create'),
    path('manage/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('manage/delete/<int:pk>/', views.user_delete, name='user_delete'),
]
