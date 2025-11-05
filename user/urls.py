from django.urls import path

from user.views import UserListView, CreateUserView, UpdateUserView, DeleteUserView

urlpatterns = [

    path('', UserListView.as_view(), name= 'user_list'),

    path('create_user/', CreateUserView.as_view(), name='create_user'),

    path('update/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),

    path('delete/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),

]
