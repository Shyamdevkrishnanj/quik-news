from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from .models import Note
from .forms import NoteForm

API_KEY = '2a4fffc220984c589f39074d28539acb'

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'news_api/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('login')
    return render(request, 'news_api/register.html')

@login_required
def home(request):
    country = request.GET.get('country')
    category = request.GET.get('category')
    articles = []

    if country:
        url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
    elif category:
        url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?apiKey={API_KEY}'
    
    response = requests.get(url)
    data = response.json()
    if 'articles' in data:
        articles = data['articles']

    # Get saved notes
    notes = request.user.profile.notes if hasattr(request.user, 'profile') else ''

    context = {
        'articles': articles,
        'notes': notes,
    }
    return render(request, 'news_api/home.html', context)

@login_required
def update_notes(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False) 
            note.user = request.user  
            note.save()  
            return redirect('view_notes')  
    else:
        form = NoteForm()

    return render(request, 'news_api/update_notes.html', {'form': form})


@login_required
def view_notes(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')  
    return render(request, 'news_api/view_notes.html', {'notes': notes})