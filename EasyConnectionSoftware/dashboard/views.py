from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupUserForm
from .models import UserForm,FormSample,ROLES,FormTransition
import json
import base64
from django.core.files.storage import FileSystemStorage
from django.db.models import Q


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

    for form in user_forms:
        form.sample.transitions = json.loads(form.sample.transitions)

    return render(request, 'dashboard/forms.html',{'page':'forms','user_forms':user_forms, 'form_samples':all_sample_forms})

def dashboard_new_form(request,form_title):
    if not request.user.is_authenticated:
        return redirect("login")
    
    form_sample = FormSample.objects.filter(title=form_title).first()

    if request.method == "POST":
        
        finaldict = {}
        print(request.FILES)
        for filename, file in request.FILES.items():
            print(file)
            fs = FileSystemStorage()
            file_name = fs.save(file.name, file)
            file_url = fs.url(filename)

            finaldict[filename]=file_url

        for key, value in dict(request.POST).items():
            if key == "csrfmiddlewaretoken":
                continue
            if request.FILES.get(key, False):
                file = request.FILES[key]
                print("sdf")
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_url = fs.url(filename)

                finaldict[key]=file_url
            else:
                finaldict[key] = value
        # print(finaldict)
        userform = UserForm.objects.create(created_by=request.user,sample=form_sample,fields=finaldict)

        tranisitions = [None,]
        # print(json.loads(form_sample.transitions))
        for trn in json.loads(form_sample.transitions):
            tranisition = FormTransition.objects.create(form=userform,receivers_role=trn)
            tranisitions.append(tranisition)
            userform.all_transitions.add(tranisition)
            # print(trn)
        tranisitions.append(None)
        
        for prev, current, nxt in zip(tranisitions, tranisitions[1:], tranisitions[2:]):
            # print("HEREE: " + str(prev if prev else '') + "|"+ str(current if current else ''))
            current.prev_transition = prev if prev else None
            current.next_transition = nxt if nxt else None
            current.save()

        userform.current_transition = tranisitions[1]
        userform.save()

        # print(finaldict)
        return redirect("forms")

    
    
    for field in form_sample.fields:
        if field["field_type"] == 'radio' or field["field_type"] == 'checkbox':
            field['extra_details'] = field['extra_details'].split('\n')
    return render(request, 'dashboard/newform.html',{'page':'forms-admin','form_title':form_sample.title,'form_description':form_sample.description,"fields":form_sample.fields})
    



def new_form_admin(request):
    if not request.user.is_authenticated:
        return redirect("login")
    ROLES_filtered = []
    for r1, r2 in ROLES:
        ROLES_filtered.append(r1)
    return render(request, 'dashboard/newform-admin.html',{'page':'forms-admin','roles':ROLES_filtered})

def dashboard_forms_admin(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        if (not request.POST["fields"]) or  (not request.POST["title"]) or (not request.POST["description"]):
            return HttpResponseBadRequest("One or more fields are not filled")

        fields = json.loads(request.POST["fields"])
        sample = FormSample.objects.create(fields=fields,description=request.POST["description"],title=request.POST["title"],transitions=request.POST['trns'])

        return redirect("forms-admin")
    
    if request.method == "GET":
        all_sample_forms = list(FormSample.objects.all())
        return render(request, 'dashboard/forms-admin.html',{'page':'forms-admin',"formsamples":all_sample_forms})

def dashboard_form_inbox(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        transition = UserForm.objects.get(pk=request.POST['formid']).current_transition
        if request.POST['comment']:
            transition.comment=request.POST['comment']
            
        print(request.POST)
        if request.POST['action'] == 'accept':
            transition.status = 'ac'
            transition.sign = request.POST['sign']
            transition.save()
            UserForm.objects.filter(pk=request.POST['formid']).update(current_transition=transition.next_transition) 
            if not transition.next_transition:
                UserForm.objects.filter(pk=request.POST['formid']).update(current_transition=None,status='sm') 


        elif request.POST['action'] == 'sendback':
            if not transition.prev_transition:
                return HttpResponseBadRequest()
            transition.status = 'sb'
            transition.save()
            UserForm.objects.filter(pk=request.POST['formid']).update(current_transition=transition.prev_transition) 

        elif request.POST['action'] == 'decline':
            transition.status = 'dc'
            transition.save()
            UserForm.objects.filter(pk=request.POST['formid']).update(current_transition=None,status='dc') 
            
        elif request.POST['action'] == 'edit':
            transition.status = 'edit'
            transition.save()
            UserForm.objects.filter(pk=request.POST['formid']).update(current_transition=None,status='edit')


        return redirect("forms-inbox")

    forms_inbox = list(UserForm.objects.filter(current_transition__receivers_role = request.user.role))

    submitted_forms = list(UserForm.objects.filter(status='sm'))
    if submitted_forms:
        for form in submitted_forms:
            if form.all_transitions.filter(receivers_role=request.user.role):
                forms_inbox.append(form)

    decliend_forms = list(UserForm.objects.filter(status='dc'))
    if decliend_forms:
        for form in decliend_forms:
            if form.all_transitions.filter(receivers_role=request.user.role):
                forms_inbox.append(form)

    if forms_inbox:
        for form in forms_inbox:
            form.fields = form.fields
    return render(request, 'dashboard/forms-inbox.html',{"forms_inbox":forms_inbox,'page':'forms-inbox'})

def dashboard_update_form(request,form_id):
    finaldict = {}
    for key, value in dict(request.POST).items():
        if key == "csrfmiddlewaretoken":
            continue
        finaldict[key] = value

    current_transition = UserForm.objects.get(pk=form_id).all_transitions.filter(status='edit').first()
    

    UserForm.objects.filter(pk=form_id).update(fields=finaldict,current_transition=current_transition,status='og')

    return redirect('forms')

def dashboard_forms_admin_update(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "GET":
       FormSample.objects.get(pk = request.GET['pk']).delete()
       return redirect('forms-admin')