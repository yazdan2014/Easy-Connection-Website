from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard_oc_tasks, name="oc-tasks"),
    path("update/", views.update_task, name="oc-update"),
    path("close/", views.close_task, name="oc-close"),

    path("admin/", views.oc_admin , name="oc-admin"),

]