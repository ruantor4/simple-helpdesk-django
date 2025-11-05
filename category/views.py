from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

import category
from category.models import Category

class CategoryListView(LoginRequiredMixin, View):

    def get(self, request:HttpRequest) -> HttpResponse:
        try:
            categories = Category.objects.all()

        except Exception as e:
            messages.error(request, f"Erro ao carregar categorias {str(e)}")
            categories = []

        return render(request, 'category/list.html', {'categories': categories})


class CreateCategoryView(LoginRequiredMixin, View):

    def get(self, request:HttpRequest) -> HttpResponse:
        try:
            return render(request, 'category/create.html')
        except Exception as e:
            messages.error(request, "Erro ao carregar pagina")

    def post(self, request:HttpRequest) -> HttpResponse:
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = Category(name=name, description=description)
        try:
            category.save()
            messages.success(request, "Categoria criada com sucesso")
            return redirect('category_list')

        except Exception as e:
            messages.error(request, f"Erro ao criar categoria {str(e)}")
            return redirect('category_list')


class UpdateCategoryView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        try:
            categories = get_object_or_404(Category, id=category_id)
            return render(request, 'category/create.html', {'categories': categories})
        except Exception as e:
            messages.error(request, "Erro ao exibir a página")
            return redirect('category_list')

    def post(self, request:HttpRequest, category_id) -> HttpResponse:
        categories= get_object_or_404(Category, id=category_id)
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        try:
            categories.name = name
            categories.description = description

            category.save()
            messages.success(request, "Categoria atualizada com sucesso")
            return redirect('category_list')

        except Exception as e:
            messages.error(request, "Erro ao atualizar categoria")
            return redirect('category_list', category_id=category_id)


class DeleteCategoryView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        try:
            categories = get_object_or_404(Category, id=category_id)
            return render(request, 'category/create.html', {'categories': categories})

        except Exception as e:
            messages.error(request, "Erro ao deletar categoria")
            return redirect('category_list')

    def post(self, request, category_id):
        try:
            categories = get_object_or_404(Category, id=category_id)
            categories.delete()
            messages.error(request, "Categoria deletada com sucesso")
            return redirect('category_list')

        except Exception as e:
            messages.error(request, "Erro ao deletar categoria")
            return redirect('category_list', category_id=category_id)







