from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

import ticket
from comment.models import Comment
from ticket.models import Ticket


class CommentListView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            comments = Comment.objects.all().order_by('-date')

        except DatabaseError:
            messages.error(request, "Erro ao acessar o banco de dados")
            comments = []

        except Exception as e:
            messages.error(request, f"Erro inesperado ao carregar comentários: {e}")
            comments = []

        return render(request, 'comment/list.html', {'comments': comments})


class CreateCommentView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest, ticket_id: int) -> HttpResponse:

        try:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            text = request.POST.get('text')

            if not text or text.strip() == '':
                messages.error(request, "O comentário não pode ser vazio.")

            Comment.objects.create(
                text=text.strip(),
                user=request.user,
                ticket=ticket
            )
            messages.success(request, "Comentário adicionado com sucesso.")
            return redirect('ticket-detail', ticket_id=ticket_id)

        except DatabaseError:
            messages.error(request, "Erro ao salvar comentário no banco de dados")

        except Exception as e:
            messages.error(request,f"Erro inesperado ao adicionar comentário: {e}")

        return redirect('ticket_detail', ticket_id=ticket_id)

class UpdateCommentView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, comment_id: int) -> HttpResponse:

            comment = get_object_or_404(Comment, id=comment_id)

            if comment.user != request.user:
                messages.error(request, "Você não tem permissão para editar este comentário.")
                return redirect('ticket_detail', ticket_id=comment.ticket.id)

            new_text = request.POST.get('text')
            if not new_text.strip():
                messages.error(request, "O comentário não pode ser vazio.")
                return redirect('ticket_detail', ticket_id=comment.ticket.id)

            try:
                comment.text = new_text
                comment.save()
                messages.warning("O comentário não pode estar vazio.")
                return redirect('ticket_detail', ticket_id=comment.ticket.id)

            except Exception as e:
                messages.error(request,f"Erro ao atualizar comentário: {e}")

            return redirect('ticket_detail', ticket_id=comment.ticket.id)

class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, comment_id: int) -> HttpResponse:
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.user != request.user:
            messages.error(request, "Você não tem permissão para excluir este comentário.")
            return redirect('ticket_detail', ticket_id=comment.ticket.id)

        try:
            comment.delete()
            messages.success(request, "Comentários excluido com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir o comentário: {e}")

        return redirect('ticket_detail', ticket_id=comment.ticket.id)








