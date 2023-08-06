from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()

    # Check if user is logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log in
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('website:home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('website:home')
    return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('website:home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #Save user to database
            form.save()
            # Get username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authenticate and log in
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered.")
            return redirect('website:home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': record})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('website:home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, "Record deleted.")
        return redirect('website:home')
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('website:home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added.")
                return redirect('website:home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('website:home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record updated.")
                return redirect('website:home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('website:home')