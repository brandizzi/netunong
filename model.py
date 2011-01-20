from django.db import models

class Organization(models.Model):
    name = models.CharField(maxlength=200)
    description = models.CharField()

class Project(models.Model):
    name = models.CharField(maxlength=200)
    description = models.CharField()
    organization = models.ForeignKey(Organization)

class Task(models.Model):
    name = models.CharField(maxlength=200)
    description = models.CharField()
    project = models.ForeignKey(Project)

class WorkingPeriod(models.Model):
    activity = models.CharField(maxlength=500)
    task = models.ForeignKey(Task)
    start = models.TimeField()
    end = models.TimeField()
