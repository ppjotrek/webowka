from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Drug, Patient, ActiveSubstance, AddedSubstance, DrugManager, PatientManager
from django.core.paginator import Paginator
from django.utils import timezone
import datetime



def registerPage(request):
    '''
    Funkcja renderująca stronę rejestracji i obsługująca formularz rejestracji.
    Formularz jest generowany automatycznie przez Django, za pomocą UserCreateForm.
    '''
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utworzono konto dla użytkownika ' + form.cleaned_data.get('username') + '. Możesz się teraz zalogować.')
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)

def loginPage(request):
    '''
    Funkcja renderująca stronę logowania i obsługująca formularz logowania.
    '''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Nazwa użytkownika lub hasło są nieprawidłowe.')
    context = {'form': None}
    return render(request, 'login.html', context)

def logoutUser(request):
    '''
    Funkcja wylogowująca użytkownika.
    '''
    logout(request)
    return redirect('login')

def home(request):
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        context = {'drugs': Drug.objects.all(), 'patients' : Patient.objects.all()}
        return render(request, 'home.html', context)

def listPage(request):
    '''
    Funkcja renderująca stronę z listą leków.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        p = Paginator(Drug.objects.all(), 5)
        page = request.GET.get('page')
        drugs = p.get_page(page)
        context = {'drugs': drugs}
        return render(request, 'list.html', context)

def patientsList(request):
    '''
    Funkcja renderująca stronę z listą pacjentów.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        p = Paginator(Patient.objects.all(), 5)
        page = request.GET.get('page')
        patients = p.get_page(page)
        context = {'patients': patients}
        return render(request, 'patients.html', context)

def account(request):
    '''
    Funkcja renderująca stronę konta użytkownika.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        context = {}
        return render(request, 'account.html', context)

def patient(request, patient_id):
    '''
    Funkcja renderująca stronę z informacjami o pacjencie.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        context = {'patient' : Patient.objects.get(id=patient_id), 'drugs' : Drug.objects.all(), 'patients' : Patient.objects.all()}
        return render(request, 'patient.html', context)

def drug(request, drug_id):
    '''
    Funkcja renderująca stronę z informacjami o leku.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        context = {'drug' : Drug.objects.get(id=drug_id), 'patients' : Patient.objects.all()}
        return render(request, 'drug.html', context)

def addDrug(request):
    '''
    Funkcja renderująca stronę dodawania leku.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        context = {}
        return render(request, 'add_drug.html', context)

def addPatient(request):
    '''
    Funkcja renderująca stronę dodawania pacjenta.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        context = {}
        return render(request, 'add_patient.html', context)

def treatment(request):
    '''
    Funkcja renderująca stronę z leczeniem pacjenta.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        if request.method == 'POST':
            patient_id = request.POST.get('patient')
            drug_id = request.POST.get('drug')
            drug_time = request.POST.get('duration')
            dose = request.POST.get('dose')
            today = timezone.now().date()
            drug_end_date = today + datetime.timedelta(days=int(drug_time))

            patient = Patient.objects.get(id=patient_id)
            drug = Drug.objects.get(id=drug_id)
            if patient.current_drugs is not None:
                if drug.main_active_substance in patient.allergies_for_active.all() or drug.other_substances in patient.allergies_for_added.all():
                    messages.warning(request, 'Pacjent jest uczulony na jedną z substancji zawartych w leku. Nie można przepisać leku. Jeśli naprawdę uważasz, że ten lek jest konieczny, skonsultuj się z pacjentem.')
                    return redirect('patients')
                elif patient.current_drugs == drug:
                    messages.info(request, 'Pacjent już przyjmuje ten lek.')
                    return redirect('patients')
                else:
                    patient.current_drugs = drug
                    patient.drug_end_date = drug_end_date
                    print("Drug changed!")
                    treatment_plan = patient.treatment_plan
                    patient.treatment_plan = "" + str(treatment_plan) + str(drug) + " dawka: " + str(dose) + " (od " + str(today) + " do " + str(drug_end_date) + ")"
                    patient.save()
                    print(patient.treatment_plan)
                    messages.success(request, 'Przypisano nowy lek.')
                    return redirect('patients')
            else:
                if drug.main_active_substance in patient.allergies_for_active.all() or drug.other_substances in patient.allergies_for_added.all():
                    return redirect('confirm', patient_id=patient_id)
                else:
                    patient.current_drugs = drug
                    patient.drug_end_date = drug_end_date
                    patient.treatment_plan = "" + str(drug) + " dawka: " + str(dose) + " (od " + str(today) + " do " + str(drug_end_date) + ")"
                    patient.save()
                    messages.success(request, 'Przypisano nowy lek.')
                    return redirect('patients')


        context = {'patients' : Patient.objects.all(), 'drugs' : Drug.objects.all(), 'patients' : Patient.objects.all()}
        return render(request, 'treatment.html', context)

def registerPatient(request):
    '''
    Funkcja renderująca stronę z rejestracją pacjenta.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        if request.method == 'POST':
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            birth_date = request.POST.get('birth_date')
            pesel = request.POST.get('pesel')
            allergies_for_active = request.POST.get('allergies_for_active').lower()
            allergies_for_added = request.POST.get('allergies_for_added').lower()

            patient = Patient.objects.create(name=name, surname=surname, birth_date=birth_date, pesel=pesel)
            if ActiveSubstance.objects.filter(act_sub_name=allergies_for_active).exists():
                patient.allergies_for_active.add(ActiveSubstance.objects.get(act_sub_name=allergies_for_active))
            else:
                patient.allergies_for_active.add(ActiveSubstance.objects.create(act_sub_name=allergies_for_active, description='Brak opisu'))
            if AddedSubstance.objects.filter(sub_name=allergies_for_added).exists():
                patient.allergies_for_added.add(AddedSubstance.objects.get(sub_name=allergies_for_added))
            else:
                patient.allergies_for_added.add(AddedSubstance.objects.create(sub_name=allergies_for_added, description='Brak opisu'))
            patient.save()

            return redirect('patients')
        context = {}
        return render(request, 'register_patient.html', context)

def editDrugs(request):
    '''
    Funkcja renderująca stronę z edycją leków.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        if request.method == 'POST':
            drug_name = request.POST.get('drug_name')
            description = request.POST.get('description')
            main_active_substance = request.POST.get('active_substance').lower()
            other_substances = request.POST.get('other_substances').lower()

            if ActiveSubstance.objects.filter(act_sub_name=main_active_substance).exists():
                drug = Drug.objects.create(drug_name=drug_name, main_active_substance=ActiveSubstance.objects.get(act_sub_name=main_active_substance), description=description)
            else:
                drug = Drug.objects.create(drug_name=drug_name, main_active_substance=ActiveSubstance.objects.create(act_sub_name=main_active_substance, description='Brak opisu'), description=description)
            if other_substances != "":
                other_substances_list = other_substances.split(', ')
                for substance in other_substances_list:
                    if AddedSubstance.objects.filter(sub_name=substance).exists():
                        drug.other_substances.add(AddedSubstance.objects.get(sub_name=substance))
                    else:
                        drug.other_substances.add(AddedSubstance.objects.create(sub_name=substance, description='Brak opisu'))
            drug.save()

            return redirect('list')
        return render(request, 'edit_drugs.html')

def editPatient(request, patient_id):
    '''
    Funkcja renderująca stronę z edycją pacjenta.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        context = {"patient": Patient.objects.get(id=patient_id)}
        return render(request, 'edit_patient.html', context)

def deletePatient(request, patient_id):
    '''
    Funkcja usuwająca pacjenta.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        patient_instance = Patient.objects.get(id=patient_id)

        if request.method == 'POST':
            patient_instance.delete()
            return redirect('patients')

        return render(request,
                    'delete_patient.html',
                    {'patient': patient_instance})

def deleteDrug(request, drug_id):
    '''
    Funkcja usuwająca lek.
    '''
    if not request.user.is_authenticated: 
        return redirect('login')
    else:
        drug_instance = Drug.objects.get(id=drug_id)

        if request.method == 'POST':
            drug_instance.delete()
            return redirect('list')

        return render(request,
                    'delete_drug.html')