from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['assigned_to', 'title', 'description', 'duration']
