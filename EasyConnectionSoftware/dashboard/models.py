from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
import json
from OCT.models import OCT

# Create your models here.
ROLES = (
        ('CEO', 'CEO'),
        ('Chief Officer', 'Chief Officer'),
        ('CEO Deligate', 'CEO Deligate'),

        ('CFO', 'CFO'),
        ('Accountant', 'Accountant'),

        ('Business Development Manager', 'Business Development Manager'),
        ('Business Development Specialist', 'Business Development Specialist'),
        ('Marketing Moderator', 'Marketing Moderator'),
        ('Marketing Specialist', 'Marketing Specialist'),

        ('IT Specialist', 'IT Specialist'),

        ('Technical Moderator', 'Technical Moderator'),
        ('Subline Chain Technation(Logistic)', 'Subline Chain Technation(Logistic)'),
        ('Factory', 'Factory'),
        ('QC Technation', 'QC Technation'),
    )

class User(AbstractUser):
    email = models.CharField(max_length=80,unique=True)
    username = models.CharField(max_length=45,unique=True)
    
    first_name = models.CharField(max_length=45)
    last_name =  models.CharField(max_length=45)

    role = models.CharField(max_length=45, choices=ROLES)

    USERNAME_FIELD="username"
    REQUIRED_FIELDS=['email',"first_name","last_name","role"]
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            obj = super(User, self).save(*args, **kwargs)
            if not OCT.objects.filter(user=self).exists():
                OCT.objects.create(user=self)
            return obj
        

        return super(User, self).save(*args, **kwargs)
    
class FormTransition(models.Model):
    form = models.ForeignKey("UserForm", on_delete=models.CASCADE , null=True)
    # receiver_user = models.ForeignKey("User", related_name='receiver' , on_delete=models.CASCADE , null=True)
    receivers_role = models.CharField(max_length=150, choices=ROLES,null=True)

    next_transition = models.ForeignKey('self',on_delete=models.CASCADE , null=True)

    sender_user = models.ForeignKey("User", related_name='sender' , on_delete=models.CASCADE, null=True)

    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    # def save(self, *args, **kwargs):
    #     if not self.pk and not self.receiver_role:
            
    #         self.receiver_role = self.receiver_user
    #         obj = super(FormTransition, self).save(*args, **kwargs)
    #         return obj
    #     return super(FormTransition, self).save(*args, **kwargs)


class UserForm(models.Model):
    created_by = models.ForeignKey("User", related_name='created_by' , on_delete=models.CASCADE)
    sample = models.ForeignKey("FormSample",related_name ="sample", on_delete=models.CASCADE)
    descrition = models.TextField()
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    current_receiver = models.ForeignKey("User", related_name='current_receiver', on_delete=models.SET_NULL,blank=True, null=True)

    fields = models.JSONField(null=True) # Type: Value

    current_transition = models.OneToOneField(FormTransition, on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.created_by.username + "/" + self.title

class FormSample(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    fields = models.JSONField(null=True) # Type: , Value:
    transitions = models.JSONField(null=True)
    
