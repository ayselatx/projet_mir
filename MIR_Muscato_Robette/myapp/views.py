from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html",{})

def indexation(request):
    return render(request, "indexation.html",{})

def recherche(request):
    return render(request, "recherche.html",{})