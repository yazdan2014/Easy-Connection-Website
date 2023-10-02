from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path("signup/", views.signup_user, name="signup"),
    path("logout/", views.logout_user, name="logout"),
    
    path("forms/", views.dashboard_forms, name="forms"),
    path("forms/<str:form_title>", views.dashboard_new_form, name="forms"),

    path("forms-admin/", views.dashboard_forms_admin, name="forms-admin"),
    path("forms-admin/new", views.new_form_admin, name="newform"),

    
    path("", views.dashboard, name="dashboard")
]