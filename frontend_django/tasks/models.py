from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.assigned_to.username})"
