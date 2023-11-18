from django.urls import path

from . import views

urlpatterns = [
    path("suggestion/", views.suggestion_form, name="suggestions"),
    path("suggestion/add/", views.add_new_suggestion, name="add-suggestions"),

    
]