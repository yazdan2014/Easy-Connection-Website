from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard_oc_tasks, name="oc-tasks"),
    path("update/", views.update_task, name="oc-update"),
]