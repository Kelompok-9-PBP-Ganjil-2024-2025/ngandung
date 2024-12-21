from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.

def register(request):
    # Return to the "/" if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('/')

    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "id": user.id,
                "username": user.username,
                "is_superuser": user.is_superuser,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
        
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            # Opsional: Tambahkan pesan menggunakan messages framework
            messages.error(request, 'Username atau password salah.')
    else:
        form = AuthenticationForm(request)
    
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('authentication:login')