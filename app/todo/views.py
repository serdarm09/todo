from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo
from django.core.paginator import Paginator
from todo.forms import TodoForm

def home(request):
    """Ana sayfa - Giriş yapmışsa todo'larını göster"""
    if request.user.is_authenticated:
        # Giriş yapmış kullanıcının todo'ları
        todos = Todo.objects.filter(user=request.user)
        context = {
            'todos': todos,
            'todo_count': todos.count(),
            'completed_count': todos.filter(status='completed').count(),
            'pending_count': todos.filter(status='pending').count(),
        }
        return render(request, 'todo/home.html', context)
    else:
        return render(request, 'todo/home.html')

def login_view(request):
    """Kullanıcı giriş sayfası"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Hoş geldiniz {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
    
    return render(request, 'todo/login.html')

def register_view(request):
    """Kullanıcı kayıt sayfası"""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST.get('password_confirm', '')
        
        # Basit validasyon
        if password != password_confirm:
            messages.error(request, 'Şifreler eşleşmiyor!')
            return render(request, 'todo/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten alınmış!')
            return render(request, 'todo/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta zaten kayıtlı!')
            return render(request, 'todo/register.html')
        
        # Kullanıcı oluştur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, 'Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
        return redirect('login')
    
    return render(request, 'todo/register.html')

@login_required
def todo_list(request):
    """Kullanıcının tüm todo'larını listele"""
    todos = Todo.objects.filter(user=request.user)
    
    # Filtreleme
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    page_number = request.GET.get('page', 1)
    
    if status_filter:
        todos = todos.filter(status=status_filter)
    if priority_filter:
        todos = todos.filter(priority=priority_filter)

    # Sayfalama
    paginator = Paginator(todos, 10)  # Sayfa başına 10 todo göster
    page_obj = paginator.get_page(page_number)

    
    context = {
        'todos': todos,
        'page_obj': page_obj,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    return render(request, 'todo/todo_list.html', context)

@login_required
def todo_detail(request, id):
    """Spesifik todo detayı"""
    todo = get_object_or_404(Todo, id=id, user=request.user)
    
    context = {
        'todo': todo,
    }
    return render(request, 'todo/todo_detail.html', context)

@login_required
def todo_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date', None)
        
        # Boş due_date'i None yap
        if due_date == '':
            due_date = None
        
        todo = Todo.objects.create(
            user=request.user,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        
        messages.success(request, f'"{title}" todosu oluşturuldu!')
        return redirect('home')
    
    return render(request, 'todo/todo_create.html')

@login_required
def todo_update_status(request, id):
    """Todo durumunu güncelle (tamamlandı/bekliyor)"""
    if request.method == 'POST':
        todo = get_object_or_404(Todo, id=id, user=request.user)
        new_status = request.POST.get('status')
        
        if new_status in ['pending', 'completed']:
            todo.status = new_status
            todo.save()
            messages.success(request, f'Todo durumu güncellendi!')
        
        return redirect('todo_list')
    
    return redirect('todo_list')

def logout_view(request):
    """Kullanıcı çıkış""" #basit düzey
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız!')
    return redirect('home')

def search(request):
##arama 
    if "q" in request.GET and request.GET["q"] != "" and request.user.is_authenticated:
        q = request.GET["q"]
        todos = Todo.objects.filter(title__icontains=q, user=request.user)
        print(todos)
        return render(request, "todo/search.html", {"todos": todos, "query": q})
    else:
        return render(request, "todo/home.html")


@login_required
def todocreate(request):
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            due_date = form.cleaned_data['due_date']
            priority = form.cleaned_data['priority']
            
            Todo.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority
            )
            messages.success(request, f'"{title}" todosu oluşturuldu!')
            return redirect('home')
    return render(request, 'todo/todocreate.html', {'form':form})