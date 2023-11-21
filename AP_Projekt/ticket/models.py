import uuid
from django.db import models
from users.models import User

class Ticket(models.Model):
    ticket_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField(default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='ticket_images/', null=True, blank=True)
    status_choices = (
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed')

    )
    ticket_status = models.CharField(choices=status_choices, max_length=120)

    def _str_(self):
        return self.title
    
# Create your models here.
