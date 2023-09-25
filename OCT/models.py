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
    def __str__(self):
        return self.goal

class DailyTasks(models.Model):
    topic = models.CharField(max_length=150,unique=True)
    description = models.TextField()
    estimated_time = models.CharField(max_length=150)
    goal_related_to = models.ForeignKey('MonthlyTasks',related_name='goal_related_to',on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.topic
    
