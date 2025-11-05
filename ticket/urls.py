from django.urls import path

from core.views import HomeView
from ticket.views import TicketDetailView, TicketListView

urlpatterns = [

    path('', TicketListView.as_view(), name='ticket_list'),

    path('<int:ticket_id>/', TicketDetailView.as_view(), name='ticket_detail'),

]
