"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from myBotVK.views import get_message as bot
from myBotVK.views import admin as bot_admin
from myBotVK.views import script as script
from myBotVK.views import client_server as cl_ser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('botVK/', bot),
    path('bot_admin/', bot_admin),
    path('bot_admin/script.js/', script),
    path('client_server/', cl_ser)
]
