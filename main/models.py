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


class ContactMessage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sender_name = models.CharField(max_length=120)
    sender_org = models.CharField(max_length=150, blank=True)
    sender_contact = models.CharField(max_length=150)
    topic = models.CharField(max_length=100, default="Kolaborasi Proyek")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender_name} - {self.topic}"
