from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from user.utils import updateUserValidation, passwordValidation, createUserValidation


class UserListView(LoginRequiredMixin,View):
    def get(self, request:HttpRequest) -> HttpResponse:
        try:
            userObj = User.objects.all()
            return render(request, 'user/user_list.html', {'userObj': userObj})
        except Exception as e:
            messages.error(request, "Erro ao carregar lista de usuários")
            return redirect('home')


class CreateUserView(LoginRequiredMixin,View):
    def get(self, request:HttpRequest) -> HttpResponse:
        try:
            return render(request, 'user/user_form.html')

        except IntegrityError:
            messages.error(request, "Erro de integridade no banco de dados")
            return redirect('user_list')

        except Exception as e:
            messages.error(request, "Erro ao buscar dados no banco")
            return redirect('user_list')

    def post(self, request:HttpRequest) -> HttpResponse:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not createUserValidation(request, username, email, password):
            return redirect('create_user')

        if not passwordValidation(request, password):
            return redirect('create_user')

        try:
            with transaction.atomic():
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
            messages.success(request, "Usuario criado com sucesso")
            return redirect('user_list')

        except ValidationError:
            messages.error(request, "Preencha os campos corretamente")
            return redirect('user_list')

        except IntegrityError:
            messages.error(request, "Erro de integridade no banco")
            return redirect('user_list')

        except Exception as e:
            messages.error(request, f"Ocorreu um erro inesperado:{str(e)} ")
            return redirect('user_form')


class UpdateUserView(LoginRequiredMixin,View):

    def get(self, request:HttpRequest, user_id) -> HttpResponse:
        try:
            userObj = get_object_or_404(User, id=user_id)
            return render(request, 'user/user_form.html', {'userObj': userObj})

        except IntegrityError:
            messages.error(request, "Erro de integridade no banco")
            return redirect('user_list')

        except Exception as e:
            messages.error(request, f"Ocorreu um erro inesperado:{str(e)}")
            return redirect('user_list')

    def post(self, request:HttpRequest, user_id) -> HttpResponse:
        userObj = get_object_or_404(User, id=user_id)
        username = request.POST.get('username','').strip()
        email = request.POST.get('email','').strip()
        password = request.POST.get('password', '').strip()

        if not updateUserValidation(request, userObj, username, email):
            return render(request, 'user/user_form.html', {'userObj': userObj})

        if not passwordValidation(request, password):
            return render(request, 'user/user_form.html', {'userObj': userObj})

        try:
            userObj.username = username
            userObj.email = email

            if password:
                userObj.set_password(password)

            userObj.save()
            messages.success(request, "Usuário atualizado com sucesso")
            return redirect('user_list')

        except ValidationError:
            messages.error(request, "Preencha os campos corretamente")
            return redirect('user_list')

        except IntegrityError:
            messages.error(request, "Erro de integridade no banco")
            return redirect('user_list')

        except Exception as e:
            messages.error(request, f"Ocorreu um erro inesperado:{str(e)} ")
            return redirect('user_form')


class DeleteUserView(LoginRequiredMixin, View):

    def get(self, request:HttpRequest, user_id) -> HttpResponse:
        try:
            userObj = get_object_or_404(User, id=user_id)
            return render(request, 'user/user_confirm_delete.html', {'userObj': userObj})

        except Exception as e:
            messages.error(request, "Erro ao exibir pagina")
            return redirect('user_list')

    def post(self, request:HttpRequest, user_id) -> HttpResponse:
        user = get_object_or_404(User, id=user_id)

        if user.username.lower() == 'admin':
            messages.error("Não é possivel excluir o usuário admin")
            return redirect('user_list')

        try:
            user.delete()
            messages.success(request, "Usuario deletado com sucesso")
            return redirect('user_list')

        except IntegrityError:
            messages.error(request, "Erro de integridade no banco")
            return redirect('user_list')

        except Exception as e:
            messages.error(request, f"Ocorreu um erro inesperado:{str(e)}")
            return redirect('user_list')

