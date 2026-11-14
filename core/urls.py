from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('city/<str:city_slug>/', views.city_landing, name='city_landing'),
]
