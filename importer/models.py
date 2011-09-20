from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import admin

class ImportedOrganization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    original_id = models.IntegerField()

    def __str__(self):
        return self.name
