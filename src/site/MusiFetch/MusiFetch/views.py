from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import sys
from fingerprints import fingerprints_generator

sys.path.append("..")  # Adds higher directory to python modules path.


# Done
def connection(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return render(request, 'home/login.html', {'error': 'Invalid username or password, please try again'})
    return render(request, 'home/login.html')


def register(request):
    if request.method == 'POST':
        # email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            try:
                User.objects.create_user(username, None, password)
            except:
                html = "<html><body>Erreur</body></html>"
                return HttpResponse(html)
    return render(request, 'home/register.html')


def find(request):
    if request.method == 'POST':
        ytb_link = request.POST['video_link']
        try:
            algo = fingerprints_generator.Algo()
            algo.choice("find", ytb_link)

            return render(request, 'home/find.twig', {'ytblink': ytb_link, 'occurences': algo.occurences})
        except:
            pass
    return redirect('/home')


def create(request):
    if request.method == 'GET':
        return render(request, 'home/create.html', {})

    if request.method == 'POST':
        ytb_link = request.POST['video_link']
        algo = fingerprints_generator.Algo()
        algo.choice("create", ytb_link)

    return redirect('/home')
