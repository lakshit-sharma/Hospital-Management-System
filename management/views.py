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
# ---------------- INDEX PAGE ----------------
def home(request):
    # if request.user.is_authenticated:
        # return HttpResponseRedirect('afterLogin')
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
            return render(request, 'contactUsSuccess.html')
    return render(request, 'contactUs.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US END ------------------------------
#---------------------------------------------------------------------------------

#----------- FOR CHECKING USER ROLE -----------------
def isAdmin(user):
    return user.groups.filter(name='ADMIN').exists()
def isDoctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def isPatient(user):
    return user.groups.filter(name='PATIENT').exists()

# ADMIN SECTION
def adminLandingPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request,'adminLandingPage.html')

def adminSignup(request):
    form=forms.AdminSignupForm()
    if request.method=='POST':
        form=forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            myAdminGroup = Group.objects.get_or_create(name='ADMIN')
            myAdminGroup[0].user_set.add(user)
            return HttpResponseRedirect('adminLogin')
    return render(request,'adminSignup.html',{'form':form})

#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterLoginView(request):
    if isAdmin(request.user):
        return redirect('adminDashboard')
    elif isDoctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctorDashboard')
        else:
            return render(request,'doctorPendingApproval.html')
    elif isPatient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patientDashboard')
        else:
            return render(request,'patientPendingApproval.html')


def checkLogInUser(request):
    if isAdmin(request.user):
        return redirect('adminDashboard')
    elif isDoctor(request.user):
        accountApproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountApproval:
            return redirect('doctorDashboard')
        else:
            return render(request,'doctorPendingApproval.html')
    elif isPatient(request.user):
        accountApproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountApproval:
            return redirect('patientDashboard')
        else:
            return render(request,'patientPendingApproval.html')

@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def adminDashboard(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorCount=models.Doctor.objects.all().filter(status=True).count()
    pendingDoctorCount=models.Doctor.objects.all().filter(status=False).count()

    patientCount=models.Patient.objects.all().filter(status=True).count()
    pendingPatientCount=models.Patient.objects.all().filter(status=False).count()

    appointmentCount=models.Appointment.objects.all().filter(status=True).count()
    pendingAppointmentCount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorCount':doctorCount,
    'pendingDoctorCount':pendingDoctorCount,
    'patientCount':patientCount,
    'pendingPatientCount':pendingPatientCount,
    'appointmentCount':appointmentCount,
    'pendingAppointmentCount':pendingAppointmentCount,
    }
    return render(request,'adminDashboard.html',context=mydict)


