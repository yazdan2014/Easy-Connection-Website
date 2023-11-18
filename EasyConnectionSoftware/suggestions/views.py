from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import json
import base64
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

def add_new_suggestion(request):
    return render()