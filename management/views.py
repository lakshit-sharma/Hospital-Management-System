from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from . import models,forms

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    # return HttpResponse("this is index")
    return render(request,'index.html')

#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def about_us(request):
    return render(request,'hospital/aboutus.html')

def contact_us(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'contact_us.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US END ------------------------------
#---------------------------------------------------------------------------------

