from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('list/', views.listPage, name='list'),
    path('admin/', admin.site.urls),
    path('account', views.account, name='account'),
    path('patients_list', views.patientsList, name='patients'),
    path('patient/<int:patient_id>', views.patient, name='patient'),
    path('drug/<int:drug_id>', views.drug, name='drug'),
    path('add_drug', views.addDrug, name='add_drug'),
    path('add_patient', views.addPatient, name='add_patient'),
    path('treatment', views.treatment, name='treatment'),
    path('register-patient', views.registerPatient, name='register_patient'),
    path('edit-drugs', views.editDrugs, name='edit_drugs'),
    path('edit-patient/<int:patient_id>', views.editPatient, name='edit_patient'),
    path('delete_patient/<int:patient_id>', views.deletePatient, name='delete_patient'),
    path('delete_drug/<int:drug_id>', views.deleteDrug, name='delete_drug'),
]