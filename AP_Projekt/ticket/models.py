import uuid
from django.db import models
from users.models import User
from django.conf import settings
import os

class Ticket(models.Model):
    ticket_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField(default='')
    workplace_nr = models.IntegerField(choices=[(i, str(i)) for i in range(101)], default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='ticket_images/', null=True, blank=True)
    priority_choices = (
        ('Problem nie wpływa na prace przy stanowisku', 'Problem nie wpływa na prace przy stanowisku'),
        ('Problem utrudnia pracę przy stanowisku', 'Problem utrudnia pracę przy stanowisku'),
        ('Problem uniemożliwia pracę przy stanowisku', 'Problem uniemożliwia pracę przy stanowisku'),
    )
    priority = models.CharField(choices=priority_choices, max_length=120, default='Not Affecting')
    status_choices = (
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed')

    )
    ticket_status = models.CharField(choices=status_choices, max_length=120)
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return os.path.join(settings.STATIC_URL, 'default_image.jpg')
    
    def _str_(self):
        return self.title
    

class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(default='')
    date_created = models.DateTimeField(auto_now_add=True)
    def _str_(self):
        return self.message[0:50]
# Create your models here.
