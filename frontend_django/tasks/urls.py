from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_login, name='login'),                     # Custom login
    path('admin-dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('employee-dashboard/', views.dashboard_employee, name='dashboard_employee'),
    path('all-tasks/', views.all_tasks, name='all_tasks'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
