from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('export/expense/pdf/<int:pk>/', views.export_expense_pdf, name='export_expense_pdf'),
    path('export/report/excel/', views.export_report_excel, name='export_report_excel'),
    path('clear-data/', views.clear_all_data, name='clear_all_data'),
]
