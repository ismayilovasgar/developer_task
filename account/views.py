# views.py
from django.contrib.auth import login,logout
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()        # İstifadəçi məlumatını alırıq
            login(request, user)          # İstifadəçini daxil olmuş kimi işarələyirik
            return redirect('home_page')  # Uğurlu daxil olma sonrası əsas səhifəyə yönləndiririk
        else:
            # Form səhvlərini göstəririk
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            
            return render(request, 'login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})



def register_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()                    # Yeni istifadəçini qeydiyyatdan keçiririk
            return redirect('login_view')  # Qeydiyyat uğurlu olduqda login səhifəsinə yönləndiririk
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("login_view")