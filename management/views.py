from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from . import models,forms
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.db.models import Q




# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    # return HttpResponse("this is index")
    return render(request,'index.html')

#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutUs(request):
    return render(request,'aboutUs.html')

def contactUs(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactUsSuccess.html')
    return render(request, 'contactUs.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US END ------------------------------
#---------------------------------------------------------------------------------

# ADMIN LOGIN
def adminLogin(request):
    return render(request, 'adminLogin.html')

def adminSignup(request):
    return render(request, 'adminSignup.html')

def adminLandingPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'adminLandingPage.html')
