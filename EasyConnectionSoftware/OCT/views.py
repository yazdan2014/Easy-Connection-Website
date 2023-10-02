
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import *
import json

# Create your views here.
def dashboard_oc_tasks(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if not OCT.objects.filter(user=request.user).exists():
        OCT.objects.create(user=request.user)
    
    if request.method == "POST":
        if request.POST['type'] == 'daily':
            goal = OCT.objects.filter(user=request.user).first().monthly_tasks.filter(goal=request.POST['goal']).first()
            new_daily_task = DailyTasks.objects.create(topic=request.POST['topic'],estimated_time=request.POST['estimated'],goal_related_to=goal)
            OCT.objects.filter(user=request.user).first().daily_tasks.add(new_daily_task)
            return redirect('oc-tasks')

        if request.POST['type'] == 'monthly':
            new_monthly_task = MonthlyTasks.objects.create(goal=request.POST['goal'],description=request.POST['description'],progress_percentage=request.POST['progress'])
            OCT.objects.filter(user=request.user).first().monthly_tasks.add(new_monthly_task)
            return redirect('oc-tasks')

        print(request.POST)
    
    found_oct = OCT.objects.filter(user=request.user).first()
    monthly_tasks = list(found_oct.monthly_tasks.all())
    daily_tasks = list(found_oct.daily_tasks.all())

    return render(request, 'OCT/oc-tasks.html',{'page':'oc-tasks','daily_tasks':daily_tasks,"monthly_tasks":monthly_tasks})

def update_task(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        
        if request.POST['type'] == 'daily':
            mt = OCT.objects.filter(user=request.user).first().monthly_tasks.filter(goal=request.POST['goal']).first()

            OCT.objects.filter(user=request.user).first().daily_tasks.filter(pk=request.POST['pk']).update(topic=request.POST['topic'],estimated_time=request.POST['estimated'],goal_related_to=mt,status='edt')

            return redirect('oc-tasks')

        if request.POST['type'] == 'monthly':
            OCT.objects.filter(user=request.user).first().monthly_tasks.filter(pk=request.POST['pk']).update(goal=request.POST['goal'],progress_percentage=request.POST['progress'],description=request.POST['description'])
            return redirect('oc-tasks')


    if request.method == 'GET':
        found_oct = OCT.objects.filter(user=request.user).first()
        print(request.GET['type'])
        # if request.GET['type'] == 'monthly':
        #     found_oct.monthly_tasks.filter(goal=request.GET['name']).delete()

        if request.GET['type'] == 'daily':
            found_oct.daily_tasks.filter(pk=request.GET['pk']).delete()

        # found_oct.daily_tasks.filter(id)
        return redirect("oc-tasks")
        
def close_task(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        
        if request.POST['type'] == 'daily':
            OCT.objects.filter(user=request.user).first().daily_tasks.filter(pk=request.POST['pk']).update(actual_time=request.POST['actual_time'],status='done')

            return redirect('oc-tasks')

        if request.POST['type'] == 'monthly':
            OCT.objects.filter(user=request.user).first().monthly_tasks.filter(pk=request.POST['pk']).update(goal=request.POST['goal'],progress_percentage=request.POST['progress'],description=request.POST['description'])
            return redirect('oc-tasks')


    # if request.method == 'GET':
    #     found_oct = OCT.objects.filter(user=request.user).first()
    #     print(request.GET['type'])
    #     # if request.GET['type'] == 'monthly':
    #     #     found_oct.monthly_tasks.filter(goal=request.GET['name']).delete()

    #     if request.GET['type'] == 'daily':
    #         found_oct.daily_tasks.filter(pk=request.GET['pk']).delete()

    #     # found_oct.daily_tasks.filter(id)
    #     return redirect("oc-tasks")
