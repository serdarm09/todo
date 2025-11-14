from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#Login
#Register
#Logout

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        print("deneme")
        if user is not None:
            auth_login(request, user)
            return render(request, 'home')
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı!")
    
    return render(request, 'login.html')





def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST.get('email', '')
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        # Şifre kontrolü
        if password != password_confirm:
            messages.error(request, 'Şifreler eşleşmiyor!')
            return render(request, 'register.html')
        
        # Kullanıcı adı kontrolü
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten alınmış!')
            return render(request, 'register.html')
        
        # Kullanıcı oluştur
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Hesabınız başarıyla oluşturuldu! Giriş yapabilirsiniz.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Hesap oluşturulurken her hangi bir hata oluştu!')
    
    return render(request, 'register.html')
