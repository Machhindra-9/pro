from django.shortcuts import render, redirect
from .models import recepies, User
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

@login_required(login_url="/login/")  # Decorator to restrict access to logged-in users
def recepies_view(request):
    query = request.GET.get('q', '')
    if query:
        queryset = recepies.objects.filter(recepie_name__icontains=query)
    else:
        queryset = recepies.objects.all()
    
    return render(request, 'recepies.html', context={
        'recepies': queryset,
        'query': query  # Pass query back to template
    })

@login_required(login_url="/login/") 
def update_recepies(request, id):
    queryset = recepies.objects.get(id=id)
    if request.method == 'POST':
        recepie_name = request.POST.get('recepie_name')
        recepie_description = request.POST.get('recepie_description')
        recepie_img = request.FILES.get('recepie_img')
        
        queryset.recepie_name = recepie_name
        queryset.recepie_description = recepie_description
        if recepie_img:
            queryset.recepie_img = recepie_img
        
        queryset.save()
        return redirect('/recepies/')
    
    return render(request, 'update_recepies.html', context={
        'recepie': queryset,
    })

@login_required(login_url="/login/") 
def delete_recepies(request, id):
    todel = recepies.objects.get(id=id)
    todel.delete()
    return redirect('/recepies/')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/recepies/')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'login_page.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            messages.info(request, 'ALL FIELDS ARE REQUIRED')
            return redirect('/register')
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'USERNAME NOT AVAILABLE')
            return redirect('/register')
        
        if password != confirm_password:
            messages.info(request, 'PASSWORDS DO NOT MATCH')
            return redirect('/register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.info(request, 'USER ADDED SUCCESSFULLY')
        return redirect('/login')
    
    return render(request, 'register_page.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')
