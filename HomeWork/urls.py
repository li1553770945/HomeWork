"""HomeWork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from login.views import LoginView,LogOutView,MeView
from work.views import HomeWorkView,MyHomeWorkNumView,MyHomeWorkView,SubmitView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',LoginView.as_view()),
    path('logout/',LogOutView.as_view()),
    path('me/',MeView.as_view()),
    path('homework/',HomeWorkView.as_view()),
    path('myhomeworknum/',MyHomeWorkNumView.as_view()),
    path('myhomework/',MyHomeWorkView.as_view()),
    path('submit/',SubmitView.as_view(),),
]
