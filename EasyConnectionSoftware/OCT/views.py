
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import *
from dashboard.models import User
import json
from django.http import JsonResponse
from datetime import *
from django.db.models import Q

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
    daily_tasks = list(found_oct.daily_tasks.filter(Q(created_at__gte=date.today()) | Q(status='nd')))

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
        if request.GET['type'] == 'monthly':
            found_oct.monthly_tasks.filter(pk=request.GET['id']).delete()

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

def oc_admin(request):
    if not request.user.is_authenticated:
        return redirect("login")

    
    users = list(User.objects.all())
    users_serialzed = []
    for user in users:
        oct = OCT.objects.filter(user=user).first()
        daily_done = oct.daily_tasks.filter(status='done').count()
        daily_notdone = oct.daily_tasks.count() - daily_done

        monthly_done = oct.daily_tasks.filter(status='done').count()
        monthly_notdone = oct.daily_tasks.count() - monthly_done

        

        serializer = {
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'last_login':user.last_login,
            'daily_tasks':{'done':daily_done,"notdone":daily_notdone},
            'monthly_tasks':{'done':monthly_done,"notdone":monthly_notdone},
            'id':user.id
        }
        
        users_serialzed.append(serializer)
    
    
    return render(request, 'OCT/oc-admin.html',{'page':'oc-admin','users':users_serialzed,'today':datetime.today()})


def get_dailytasks(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    this_week = int(datetime.today().strftime("%U"))
    selected_week = this_week - int(request.GET['week'])


    res_raw = OCT.objects.filter(user=request.GET['uid']).first().daily_tasks.filter(created_at__week=selected_week)
    final_res = {"Monday":[],"Tuesday":[],"Wednesday":[],"Thursday":[],"Friday":[],"Saturday":[],"Sunday":[]}
    for res in res_raw:
        serializer={
            "id":res.id,
            "status":res.get_status_display(),
            "topic":res.topic,
            "goal":res.goal_related_to.goal if res.goal_related_to else 'None',
            "estimated_time":res.estimated_time,
            "actual_time":res.actual_time,
            'checked_by_admin':res.checked_by_admin,
            "admin_comment":res.admin_comment,
            'ca_time':res.created_at.strftime("%H:%M:%S"),
            'ca_weekday':res.created_at.weekday(),
            'ca_weekdaystr':res.created_at.strftime("%A"),
            'ca_date':res.created_at.date(),
        }
        final_res[res.created_at.strftime("%A")].append(serializer)


    return JsonResponse(final_res)

def get_monthlygoals(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    this_month = datetime.today().date().month
    print(this_month)
    res_raw = list(OCT.objects.filter(user=request.GET['uid']).first().monthly_tasks.filter(created_at__month=this_month).values())
    return JsonResponse({'data':res_raw})

def check_task(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.GET['monthly']:
        MonthlyTasks.objects.filter(pk=request.GET['tid']).update(checked_by_admin=True)
    else:
        DailyTasks.objects.daily_tasks.filter(pk=request.GET['tid']).update(checked_by_admin=True)
    return JsonResponse({'data':"Successful"})


def comment_task(request):
    if not request.user.is_authenticated:
        return redirect("login")
    print(request.GET)
    if request.GET.get('type') == 'monthly':
        if request.GET.get('cmt'):
            OCT.objects.filter(user=request.user).first().monthly_tasks.filter(pk=request.GET['tid']).update(admin_comment=f"{request.GET.get('cmt')}")
        else :
            OCT.objects.filter(user=request.user).first().monthly_tasks.filter(pk=request.GET['tid']).update(admin_comment="")

    else:
        if request.GET.get('cmt'):
            OCT.objects.filter(user=request.user).first().daily_tasks.filter(pk=request.GET['tid']).update(admin_comment=f"{request.GET.get('cmt')}")
        else :
            OCT.objects.filter(user=request.user).first().daily_tasks.filter(pk=request.GET['tid']).update(admin_comment="")

    return JsonResponse({'data':"Successful"})
