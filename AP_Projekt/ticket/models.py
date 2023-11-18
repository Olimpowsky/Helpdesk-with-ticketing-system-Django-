from django.db import models
from users.models import User
import uuid  #nadaje unikalny numer dla zgłoszenia

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    status_choices = (
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed')

    )
    ticket_status = models.CharField(choices=status_choices)

    def _str_(self):
        return self.title
    
# Create your models here.
