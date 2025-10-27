from django.contrib import admin

from category.models import Category
from comment.models import Comment
from ticket.models import Ticket

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Ticket)
