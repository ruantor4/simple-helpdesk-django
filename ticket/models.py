from django.contrib.auth.models import User
from django.db import models

from category.models import Category

STATUS_TICKET = [
    ('aberto', 'Aberto'),
    ('em_andamento', 'Em Andamento'),
    ('resolvido', 'Resolvido'),
    ('fechado', 'Fechado'),
]


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=12, choices=STATUS_TICKET, default='aberto')
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ticket'
