from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='homepage'),
    path('about_us',views.about_us, name='about_us'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_signup', views.admin_signup, name='admin_signup'),
    
]
