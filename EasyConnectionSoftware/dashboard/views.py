from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupUserForm
from .models import UserForm,FormSample
import json


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return redirect('dashboard')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,'there was an error logging in, try again')
            return  render(request, 'dashboard/login.html')
    else:
        return render(request, 'dashboard/login.html')
    
def logout_user(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect("login")

def signup_user(request):
    if request.method == "POST":
        form = SignupUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request,user)
            messages.success(request,'Signed up Successfully')
            return redirect('dashboard')
        else: 
            messages.error(request,'There was an error with your form')
            return render(request, 'dashboard/signup.html', context={'form': form})
    else:
        form = SignupUserForm()

        return render(request, 'dashboard/signup.html',{"form":form})
    
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'dashboard/dashboard.html',{'page':'dashboard'})



def dashboard_forms(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    all_sample_forms = list(FormSample.objects.all())
    user_forms = UserForm.objects.filter(created_by=request.user)


    return render(request, 'dashboard/forms.html',{'page':'forms','user_forms':user_forms, 'form_samples':all_sample_forms})

def dashboard_new_form(request,form_title):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        pass
    
    form_sample = FormSample.objects.filter(title=form_title).first()
    for field in form_sample.fields:
        if field["field_type"] == 'radio' or field["field_type"] == 'checkbox':
            field['extra_details'] = field['extra_details'].split('\n')
    print(form_sample.fields)
    return render(request, 'dashboard/newform.html',{'page':'forms-admin','form_title':form_sample.title,'form_description':form_sample.description,"fields":form_sample.fields})




def new_form_admin(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'dashboard/newform-admin.html',{'page':'forms-admin'})

def dashboard_forms_admin(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        if (not request.POST["fields"]) or  (not request.POST["title"]) or (not request.POST["description"]):
            return HttpResponseBadRequest("One or more fields are not filled")
            
        fields = json.loads(request.POST["fields"])
        FormSample.objects.create(fields=fields,description=request.POST["description"],title=request.POST["title"])
        print(fields)
        return redirect("forms-admin")
    
    if request.method == "GET":
        all_sample_forms = list(FormSample.objects.all())
        return render(request, 'dashboard/forms-admin.html',{'page':'forms-admin',"formsamples":all_sample_forms})
    





