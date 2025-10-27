from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View


class UserListView(LoginRequiredMixin,View):
    def get(self, request:HttpRequest) -> HttpResponse:
        user = User.objects.all()
        return render(request, 'user/user_list.html', {'user': user})