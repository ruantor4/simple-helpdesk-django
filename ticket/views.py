from django.contrib import messages
from django.db import DatabaseError
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from ticket.models import Ticket


class TicketListView(LoginRequiredMixin, View):

    def get(self, request:HttpRequest) -> HttpResponse:

        try:
            tickets = Ticket.objects.all().select_related('category','user').order_by('-created_at')

        except DatabaseError:
            messages.error(request,"Erro ao acessar banco de dados" )
            tickets = []

        return render(request, 'ticket/ticket_list.html', {'tickets': tickets})


class TicketDetailView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):

        try:
            ticket = get_object_or_404(Ticket.objects.select_related('category','user'), id=ticket_id)
            return render(request, 'ticket/ticket_detail.html', {'ticket': ticket})

        except Exception as a:
            messages.error(request, "Erro ao exibir o ticket.")
            return redirect('ticket_list')