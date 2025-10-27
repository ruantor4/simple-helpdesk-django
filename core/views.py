from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            return render(request, 'core/home.html')

        except Exception as e:
            messages.error(request, "Erro ao carregar a pagina inicial")
            return redirect('home')


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            if request.user.is_authenticated:
                return redirect('home')
            return render(request, 'core/login.html')

        except Exception as e:
            messages.error(request, "Erro ao carregar a pagina de login.")
            return redirect('login')

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Usuário ou senha incorretos.")
                return render(request, 'core/login.html')

        except Exception as e:
            messages.error(request, "Erro inesperado ao processar login.")
            return render('login')


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            if request.user.is_authenticated:
                logout(request)
                return redirect('login')
        except Exception as e:
            messages.error(request, "Erro ao encerrar a sessão.")
            return redirect('login')
