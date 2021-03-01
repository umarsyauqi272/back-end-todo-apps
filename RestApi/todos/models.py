from django.db import models

# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=20, blank=False, unique=True)
    note = models.CharField(max_length=200, blank=False)
    priority = models.CharField(max_length=20, blank=False)
    finished = models.BooleanField(default=False)