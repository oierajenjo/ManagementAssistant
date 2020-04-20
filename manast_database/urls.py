from django.urls import path

from manast_database import views


urlpatterns = [
    path('', views.index, name='index'),
]
