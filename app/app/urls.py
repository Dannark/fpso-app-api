"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from core import views

urlpatterns = [
    path('', views.index, name="index"),
    path('vessels', views.vessel_list, name="vessel-list"),
    path('vessel/<str:vessel_code>', views.vessel, name='vessel'),
    path('equipments', views.equipments_list, name='equipment-detail'),
    path('equipment/<str:vessel_code>', views.equipment, name='equipment'),
    path('admin/', admin.site.urls)
]
