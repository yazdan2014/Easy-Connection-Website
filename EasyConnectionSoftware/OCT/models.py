from django.db import models

# Create your models here.
class OCT(models.Model):
    user = models.OneToOneField("dashboard.User", related_name='octuser' , on_delete=models.CASCADE)
    daily_tasks = models.ManyToManyField("DailyTasks",blank=True)
    monthly_tasks = models.ManyToManyField("MonthlyTasks",blank=True)


class MonthlyTasks(models.Model):
    goal = models.CharField(max_length=150,unique=True)
    progress_percentage = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ('og','On Going'),
        ('done', 'Done'),
        ('nd','Not Done')
    )
    status = models.CharField(max_length=150,choices=STATUS_CHOICES,default='og')

    def __str__(self):
        return self.goal

class DailyTasks(models.Model):
    topic = models.CharField(max_length=150,unique=True)
    estimated_time = models.CharField(max_length=150)
    actual_time = models.CharField(max_length=150, null=True,blank=True)
    goal_related_to = models.ForeignKey('MonthlyTasks',related_name='goal_related_to',on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ('jc','Just Created'),
        ('cba','Checked By Admin'),
        ('edt', 'Edited'),
        ('done', 'Done'),
        ('nd','Not Done')
    )
    
    status = models.CharField(max_length=150,choices=STATUS_CHOICES,default='jc')
    def __str__(self):
        return self.topic
    
