from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views import View

from ticket.models import Ticket


class TicketDetailView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        comments = ticket.comments.all().order_by('-date')
        return render(request, 'ticket/detail.html', {
            'ticket': ticket,
            'comments': comments
        })
