from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import DatabaseError, IntegrityError
from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from category.models import Category


class CategoryListView(LoginRequiredMixin, View):

    def get(self, request:HttpRequest) -> HttpResponse:

        try:
            categories = Category.objects.all()

        except DatabaseError:
            messages.error(request, "Erro ao acessar o banco de dados.")
            categories = []

        except Exception as e:
            messages.error(request, f"Erro inesperado ao carregar categorias: {e}")
            categories = []

        return render(request, 'category/list.html', {'categories': categories})


class CreateCategoryView(LoginRequiredMixin, View):

    def get(self, request:HttpRequest) -> HttpResponse:

        try:
            return render(request, 'category/create.html')

        except Exception:
            messages.error(request, "Erro ao carregar a página de criação de categoria.")
            return redirect('category_list')

    def post(self, request:HttpRequest) -> HttpResponse:

        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        try:
            category = Category(name=name, description=description)
            category.full_clean()
            category.save()

            messages.success(request, "Categoria criada com sucesso")
            return redirect('category_list')

        except ValidationError as e:
            messages.error(request, f"Erro de validação: {e}")

        except IntegrityError:
            messages.error(request, "Erro de integridade no banco (duplicidade ou FK inválida).")

        except DatabaseError:
            messages.error(request, "Erro ao salvar categoria no banco de dados.")

        except Exception as e:
            messages.error(request, f"Erro inesperado ao criar categoria: {e}")

        return redirect('category_list')


class UpdateCategoryView(LoginRequiredMixin, View):

    def get(self, request:HttpRequest, category_id: int) -> HttpResponse:

        try:
            category = get_object_or_404(Category, id=category_id)
            return render(request, 'category/create.html', {'category': category})

        except Http404:
            messages.error(request, "Categoria não encontrada.")

        except Exception:
            messages.error(request, "Erro ao carregar página de edição.")

        return redirect('category_list')

    def post(self, request:HttpRequest, category_id: int) -> HttpResponse:

        try:
            category= get_object_or_404(Category, id=category_id)

            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()

            category.name = name
            category.description = description

            category.full_clean()
            category.save()

            messages.success(request, "Categoria atualizada com sucesso")
            return redirect('category_list')

        except ProtectedError:
            messages.error(request, "Não é possível excluir esta categoria: há registros relacionados.")

        except ObjectDoesNotExist:
            messages.error(request, "Categoria não encontrada.")

        except DatabaseError:
            messages.error(request, "Erro ao excluir categoria no banco de dados.")

        except Exception as e:
            messages.error(request, f"Erro inesperado ao deletar categoria: {e}")

        return redirect('category_list')


class DeleteCategoryView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, category_id) -> HttpResponse:
        try:
            category = get_object_or_404(Category, id=category_id)
            return render(request, 'category/categ_confirm_delete.html', {'category': category})

        except Exception as e:
            messages.error(request, "Erro ao deletar categoria")
            return redirect('category_list')

    def post(self, request:HttpRequest, category_id) -> HttpResponse:

        try:
            category = get_object_or_404(Category, id=category_id)
            category.delete()

            messages.success(request, "Categoria deletada com sucesso")
            return redirect('category_list')

        except ObjectDoesNotExist:
            messages.error(request, "Categoria não encontrada.")

        except DatabaseError:
            messages.error(request, "Erro ao excluir a categoria.")

        except Exception as e:
            messages.error(request, f"Erro ao deletar categoria: {e}")

        return redirect('category_list')







