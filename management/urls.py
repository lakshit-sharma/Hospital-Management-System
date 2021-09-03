from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='homepage'),
    path('aboutUs',views.aboutUs, name='aboutUs'),
    path('contactUs', views.contactUs, name='contactUs'),
    path('adminLandingPage', views.adminLandingPage, name="adminLandingPage"),
    path('adminLogin', views.adminLogin, name='adminLogin'),
    path('adminSignup', views.adminSignup, name='adminSignup'),
    
]
