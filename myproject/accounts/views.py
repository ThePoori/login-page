from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def login_view(request):
    # اگر قبلاً لاگین کرده بود
    if request.user.is_authenticated:
        return redirect('/dashboard/')  # یا هر صفحه دیگه‌ای

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # اعتبارسنجی ساده
        if not username or not password:
            messages.error(request, 'لطفاً نام کاربری و رمز عبور را وارد کنید')
            return render(request, 'login.html')

        # احراز هویت کاربر
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # بعد از لاگین موفق به کجا بره
            next_url = request.GET.get('next', '/dashboard/')
            return redirect(next_url)
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید')
    return redirect('login')


# یک ویو ساده برای صفحه بعد از لاگین
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html', {
        'username': request.user.username
    })