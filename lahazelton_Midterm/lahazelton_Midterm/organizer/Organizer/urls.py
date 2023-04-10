"""Organizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Budget import views as budget_views
from Tasks import views as task_views
from Default import views as default_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', default_views.about),
    path('', default_views.home, name ='home'),
    path('tasks/', task_views.home),
    path('tasks/add', task_views.add),
    path('tasks/edit/<int:id>/', task_views.edit),
    path('tasks/completed/<int:id>/', task_views.completed),
    path('budget/', budget_views.home),
    path('budget/add', budget_views.add),
    path('budget/edit/<int:id>/', budget_views.edit),
    path('login/', default_views.user_login),
    path('join/', default_views.join),
    path('logout/', default_views.user_logout),
]
