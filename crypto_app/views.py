from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, ConverterForm, LoginForm, UpdateProfileForm
from .helpers import get_crypto_news, get_crypto_price, get_top_crypto, crypto_for_converter
from django.contrib.auth import login as auth_login


def index(request):
    news = get_crypto_news()
    if news:
        news_f_temp = [(article['title'], article['url']) for article in news]
    else:
        news_f_temp = []

    top_crypto = get_top_crypto()
    if top_crypto:
        for crypto in top_crypto:
            crypto['name'] = f"{crypto['name']} ({crypto['symbol']})"
    else:
        top_crypto = []

    paginator = Paginator(top_crypto, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'top_crypto': page_obj,
        'news': news_f_temp,
    }
    return render(request, 'index.html', context)


def crypto_news(request):
    news = get_crypto_news()
    if news:
        news_f_temp = [(article['title'], article['url']) for article in news]
    else:
        news_f_temp = []

    context = {
        'news': news_f_temp,
    }
    return render(request, 'news.html', context)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = True
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.save()
            return render(request, 'login.html')
    form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Ви успішно увійшли в обліковий запис')
                response = redirect('index')
                response.set_cookie('user_id', user.id, max_age=60 * 60 * 24 * 3)
                return response
            else:
                messages.error(request, 'Невірний логін або пароль.')
        else:
            messages.error(request, 'Невірно введені дані.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль успішно оновлено')
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Ви успішно вийшли з облікового запису')
    return redirect('index')


def converter(request):
    form = ConverterForm()
    if request.method == 'GET':
        crypto_for_converter(form)
        return render(request, 'converter.html', {'form': form})
    else:
        from_crypto = request.POST.get('from_crypto')
        amount = float(request.POST.get('amount'))
        to_crypto = request.POST.get('to_crypto')
        price = get_crypto_price(from_crypto, to_crypto)
        crypto_for_converter(form)
        if price:
            price_f = round(price * amount, 2)
            messages.info(request,
                          f'Ціна {amount} {from_crypto.upper()} у {to_crypto.upper()}: {price_f} {to_crypto.upper()}')
        else:
            messages.error(request, 'Помилка при конвертації')
        return render(request, 'converter.html', {'form': form})
