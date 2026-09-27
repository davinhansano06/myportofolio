from django.contrib.auth.models import User
from django.db import models
import uuid


class Education(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    period = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    skills = models.TextField()
    is_current = models.BooleanField(default=False)
    logo = models.CharField(max_length=255)
    starred_by = models.ManyToManyField(User,blank=True,related_name="starred_educations")

    def __str__(self):
        return self.institution
    
class Experience(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255, blank=True)
    period = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    image = models.CharField(max_length=255, blank=True)
    starred_by = models.ManyToManyField(User,blank=True,related_name="starred_experiences")

    def __str__(self):
        return self.title