

from django.contrib import admin
from django.urls import path
from management import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name=''),


    path('aboutUs', views.aboutUs),
    path('contactUs', views.contactUs),


    path('adminHomePage', views.adminHomePage),
    path('doctorHomePage', views.doctorHomePage),
    path('patientHomePage', views.patientHomePage),

    path('adminSignUp', views.adminSignUp),
    path('doctorSignUp', views.doctorSignUp,name='doctorSignUp'),
    path('patientSignUp', views.patientSignUp),
    
    path('adminLogIn', LoginView.as_view(template_name='adminLogIn.html')),
    path('doctorLogIn', LoginView.as_view(template_name='doctorLogIn.html')),
    path('patientLogIn', LoginView.as_view(template_name='patientLogIn.html')),


    path('afterLogin', views.checkLogIn,name='afterLogin'),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),


    path('adminDashboard', views.adminDashboard,name='adminDashboard'),

    path('adminDoctor', views.adminDoctorView,name='adminDoctor'),
    path('adminViewDoctor', views.adminViewDoctorView,name='adminViewDoctor'),
    path('deleteDoctorFromHospital/<int:pk>', views.deleteDoctorFromHospitalView,name='deleteDoctorFromHospital'),
    path('updateDoctor/<int:pk>', views.updateDoctorView,name='updateDoctor'),
    path('adminAddDoctor', views.adminAddDoctorView,name='adminAddDoctor'),
    path('adminApproveDoctor', views.admin_approve_doctor_view,name='adminApproveDoctor'),
    path('approveDoctor/<int:pk>', views.approve_doctor_view,name='approveDoctor'),
    path('rejectDoctor/<int:pk>', views.reject_doctor_view,name='rejectDoctor'),
    path('adminViewDoctorSpecialisation',views.adminViewDoctorSpecialisationView,name='adminViewDoctorSpecialisation'),


    path('adminPatient', views.adminPatientView,name='admin-patient'),
    path('adminViewPatient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('adminAddPatient', views.admin_add_patient_view,name='admin-add-patient'),
    path('adminApprovePatient', views.adminApprovePatientView,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('adminDischargePatient', views.adminDischargePatientView,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('adminAppointment', views.adminAppointmentView,name='admin-appointment'),
    path('adminViewAppointment', views.adminViewAppointmentView,name='admin-view-appointment'),
    path('adminAddAppointment', views.adminAddAppointmentView,name='admin-add-appointment'),
    path('adminApproveAppointment', views.adminApproveAppointmentView,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]



