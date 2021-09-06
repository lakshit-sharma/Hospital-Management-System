from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('',views.home, name='homepage'),
    path('aboutUs',views.aboutUs, name='aboutUs'),
    path('contactUs', views.contactUs, name='contactUs'),
    path('adminLandingPage', views.adminLandingPage, name="adminLandingPage"),
    path('adminSignup', views.adminSignup, name='adminSignup'),
    path('adminDashboard', views.adminDashboard, name='adminDashboard'),
    path('adminLogin', LoginView.as_view(template_name='adminLogin.html')),
    path('afterLoginView',views.afterLoginView, name='afterLoginView'),
    
]
