from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from users.forms import LoginForm


# Create your views here.


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:index')
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Disabled account'
                    )
                    return render(request, 'users/login.html')
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Username or Password invalid'
                )
                return render(request, 'users/login.html')

    return render(request, 'users/login.html', {'form': form})


def register_page(request):
    form =LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = CustomUser.objects.get(email=cd['email'])
            if user:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Account with this creadiantials already exists'
                )
                return render(request, 'users/register.html')
            else:
                user = CustomUser.objects.create_user(
                    email=cd['email'],
                    password=cd['password'],
                )
                user.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'You have successfully registered'
                )
                return render(request, 'shop:index.html')
    return render(request, 'users/register.html', {'form': form})




def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('shop:index')
