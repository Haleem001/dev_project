# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AdoptionRequest
from .utils import send_adoption_approval_email, send_adoption_rejection_email

@receiver(post_save, sender=AdoptionRequest)
def handle_adoption_request_status_change(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'approved':
            send_adoption_approval_email(instance)
        elif instance.status == 'rejected':
            send_adoption_rejection_email(instance)
