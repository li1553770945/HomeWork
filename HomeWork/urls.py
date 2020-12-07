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
from django.urls import path,include
from login.views import LoginView,LogOutView,MeView,RegisterView
from work.views import HomeWorkView,MyHomeWorkNumView,MyHomeWorkView,SubmitView,DownloadView,ExportView,DoneListView
from group.views import GroupView,MyGroupNumView,MyGroupView,GroupMembersView
import debug_toolbar
urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/login/',LoginView.as_view()),
    path('api/logout/',LogOutView.as_view()),
    path('api/me/',MeView.as_view()),
    path('api/homework/',HomeWorkView.as_view()),
    path('api/myhomeworknum/',MyHomeWorkNumView.as_view()),
    path('api/myhomework/',MyHomeWorkView.as_view()),
    path('api/submit/',SubmitView.as_view(),),
    path('api/group/',GroupView.as_view()),
    path('api/mygroup/',MyGroupView.as_view()),
    path('api/mygroupnum/',MyGroupNumView.as_view()),
    path('api/register/',RegisterView.as_view()),
    path('api/groupmembers/',GroupMembersView.as_view()),
    path('api/download/',DownloadView.as_view()),
    path('api/export/',ExportView.as_view()),
    path('api/donelist/',DoneListView.as_view()),
    path('__debug__/',include(debug_toolbar.urls))
]

