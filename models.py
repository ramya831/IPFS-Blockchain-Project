from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class SharedData(models.Model):
    data_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(User, related_name='shared_to', on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(upload_to='files/', null=True, blank=True)
    ipfs_hash = models.CharField(max_length=255)
    shared_date_time = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10)


class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('dataowner', 'DataOwner'),
        ('user', 'User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    
    

    def clean(self):
        if not self.ipfs_hash:
            raise
    ValidationError("IPFS Hash is required!")
    def __str__(self):
        return self.message
        
  
