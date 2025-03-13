from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render,redirect

# Create your views here.
CustomUser = get_user_model()


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            CustomUser.objects.filter(email=email).update(is_active=True)
            login(request, user)
            return redirect('home')

    return render(request, 'users/login.html')


def register_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.create_user(email=email, password=password)
            return redirect('login')

    return render(request, 'users/register.html')


def logout_page(request):
    logout(request)
    return redirect('login')