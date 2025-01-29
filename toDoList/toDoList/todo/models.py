from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Priority(models.Model):
    level=models.CharField(max_length=50,null=False)


class Task(models.Model):
    users = models.ManyToManyField(User, related_name='tasks')
    title = models.CharField(max_length=200)
    description=models.TextField(max_length=500, blank=True)
    isCompleted= models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    priority = models.ForeignKey(Priority, related_name='priorityLevel', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

