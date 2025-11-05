from django.urls import path
from comment.views import CreateCommentView, UpdateCommentView, DeleteCommentView

urlpatterns = [

    path('add/<int:ticket_id>/', CreateCommentView.as_view(), name='add_comment'),

    path('update/<int:comment_id>/', UpdateCommentView.as_view(), name='update_comment'),

    path('delete/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),

]
