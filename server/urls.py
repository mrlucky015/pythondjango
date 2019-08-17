from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='server-about'),
    path('monitor/', views.monitorserver, name='server-monitor'),
#    path('monitor/result/', views.monitorserverresult, name='server-monitorresult'),
    path('users/', views.users, name='server-users'),
]

