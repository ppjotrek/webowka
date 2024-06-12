from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Drug, Patient


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

    context = {'drugs': Drug.objects.all(), 'patients' : Patient.objects.all()}
    return render(request, 'home.html', context)