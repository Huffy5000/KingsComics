from django.contrib import admin
from django.urls import path,include
from .views import HomePageView,contact


app_name = 'webApp'


urlpatterns = [
    path('',HomePageView.as_view(),name='comic-home'),
    path('contact/',contact,name = "contact"),
]
