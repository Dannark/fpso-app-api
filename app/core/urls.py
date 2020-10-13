from django.urls import path
from core import views

app_name = ''

urlpatterns = [
    path('', views.index, name="index"),
    path('vessels', views.vessel_list, name="vessel-list"),
    path('vessels/create', views.vessel_create, name="vessel-create"),
    path('equipments/', views.equipments_list, name='equipment-list'),
    path('equipment/create/<str:vessel_code>',
         views.equipment_create, name='equipment-create'),
    path('equipment/update', views.equipment_update, name='equipment-update')
]
