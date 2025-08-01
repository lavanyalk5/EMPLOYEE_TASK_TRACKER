from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm

# ✅ Custom login that redirects based on role
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.is_staff:
                return redirect('dashboard_admin')
            else:
                return redirect('dashboard_employee')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

# ✅ Admin/BA Dashboard
@login_required
def dashboard_admin(request):
    if not request.user.is_staff:
        return redirect('dashboard_employee')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
    else:
        form = TaskForm()

    tasks = Task.objects.all()
    return render(request, 'dashboard_admin.html', {'form': form, 'tasks': tasks})

# ✅ Employee Dashboard
@login_required
def dashboard_employee(request):
    if request.user.is_staff:
        return redirect('dashboard_admin')

    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'dashboard_employee.html', {'tasks': tasks})

# ✅ Optional: View all tasks
@login_required
def all_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'all_tasks.html', {'tasks': tasks})

def analytics_page(request):
    return render(request, 'analytics.html')

