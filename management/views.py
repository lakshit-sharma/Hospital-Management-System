from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
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



#for showing signup/login button for admin
def adminHomePage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request,'adminHomePage.html')


#for showing signup/login button for doctor
def doctorHomePage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request,'doctorHomePage.html')


#for showing signup/login button for patient
def patientHomePage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request,'patientHomePage.html')


# ADMIN SIGNUP PAGE

def adminSignUp(request):
    form=forms.AdminSignupForm()
    if request.method=='POST':
        form=forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminLogin')
    return render(request,'adminSignUp.html',{'form':form})



# DOCTOR SIGNUP PAGE
def doctorSignUp(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorLogIn')
    return render(request,'doctorSignUp.html',context=mydict)


def patientSignUp(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'patientSignUp.html',context=mydict)



#-----------for checking user is doctor , patient or admin
def isAdmin(user):
    return user.groups.filter(name='ADMIN').exists()
def isDoctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def isPatient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def checkLogIn(request):
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
            return render(request,'patient_wait_for_approval.html')


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def adminDashboard(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'adminDashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def adminDoctorView(request):
    return render(request,'adminDoctor.html')



@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def adminViewDoctorView(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'adminViewDoctor.html',{'doctors':doctors})



@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def deleteDoctorFromHospitalView(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('adminViewDoctor')

# completed till here

@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def updateDoctorView(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('adminViewDoctor')
    return render(request,'adminUpdateDoctor.html',context=mydict)




@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def adminAddDoctorView(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('adminViewDoctor')
    return render(request,'adminAddDoctor.html',context=mydict)




@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'adminApproveDoctor.html',{'doctors':doctors})


@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('adminApproveDoctor'))


@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('adminApproveDoctor')



@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def adminViewDoctorSpecialisationView(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'adminViewDoctorSpecialisation.html',{'doctors':doctors})



@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def adminPatientView(request):
    return render(request,'adminPatient.html')



@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'adminViewPatient.html',{'patients':patients})



@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)





@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'adminAddPatient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def adminApprovePatientView(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'adminApprovePatient.html',{'patients':patients})



@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminLogin')
@user_passes_test(isAdmin)
def adminDischargePatientView(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'adminDischargePatient.html',{'patients':patients})



#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------

