from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('index/', views.index, name="index"),     
    path('logout/', views.logout_view, name="logout"),
    path('employees/', views.add_employee, name="add_employee"),
    path('master-data/', views.master_data_view, name="master_data"),
    path('employeelist/', views.employee_list, name='employee_list'),
    path('attendance/', views.mark_attendance, name="mark_attendance"),
    path('edit_attendance/', views.admin_attendance_edit, name="admin_attendance_edit"),
]
