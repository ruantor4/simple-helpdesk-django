from django.urls import path

from ticket.views import TicketDetailView

urlpatterns = [

    path('<int:ticket_id>/', TicketDetailView.as_view(), name='ticket_detail'),

]
