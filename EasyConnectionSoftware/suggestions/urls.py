from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.add_new_suggestion, name="add-suggestion"),

]