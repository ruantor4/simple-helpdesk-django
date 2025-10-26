from django.urls import path

from category import views
from core.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),



]
