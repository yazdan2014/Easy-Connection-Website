from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
import json

# Create your models here.

class User(AbstractUser):
    email = models.CharField(max_length=80,unique=True)
    username = models.CharField(max_length=45,unique=True)
    
    first_name = models.CharField(max_length=45)
    last_name =  models.CharField(max_length=45)

    ROLES = (

        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Physician', 'Physician'),

    )
    role = models.CharField(max_length=45, choices=ROLES)

    USERNAME_FIELD="username"
    REQUIRED_FIELDS=['email',"first_name","last_name","role"]
    
    def __str__(self):
        return self.username
    
class FormTransition(models.Model):
    # form = models.ForeignKey("UserForm", on_delete=models.CASCADE)
    receiver_user = models.ForeignKey("User", related_name='receiver' , on_delete=models.CASCADE)
    sender_user = models.ForeignKey("User", related_name='sender' , on_delete=models.CASCADE)
    date = models.DateTimeField()
    message = models.TextField()

    def create(self, *args):
        pass


class UserForm(models.Model):
    created_by = models.ForeignKey("User", related_name='created_by' , on_delete=models.CASCADE)
    sample = models.ForeignKey("FormSample",related_name ="sample", on_delete=models.CASCADE)
    descrition = models.TextField()
    form_id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    date = models.DateTimeField()
    status = models.CharField(max_length=50)
    current_receiver = models.ForeignKey("User", related_name='current_receiver', on_delete=models.SET_NULL,blank=True, null=True)

    fields = models.JSONField( null=True) # Type: , Value:

    transitions = models.ManyToManyField(FormTransition)
    
    def __str__(self):
        return self.created_by.username + "/" + self.title

    def setStatus(self,status):
        self.status = status

    def create(self, *args):
        pass

class FormSample(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    fields = models.JSONField( null=True) # Type: , Value:
    
