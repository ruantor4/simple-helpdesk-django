from django.contrib.auth.models import User
from django.db import models

from ticket.models import Ticket


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'comment'
        ordering = ['-date']