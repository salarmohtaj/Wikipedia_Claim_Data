from django.urls import path
from webapp import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
]
