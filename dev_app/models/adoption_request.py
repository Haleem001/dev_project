from django.db import models
from .user import User
from .children import Child

from django.utils import timezone


class AdoptionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    rejected_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically set the child's adoption status if the request is approved
        if self.pk is not None:
            original = AdoptionRequest.objects.get(pk=self.pk)
            if original.status == 'approved' and self.status == 'approved':
                raise ValueError('This adoption request has already been approved.')
            if original.status == 'rejected' and self.status == 'rejected':
                raise ValueError('This adoption request has already been rejected.')

        if self.status == 'approved':
            if self.child.is_adopted:
                raise ValueError('This child has already been adopted and cannot be adopted again.')
            self.child.is_adopted = True
            self.child.save()

        if self.status == 'approved' and not self.approved_date:
            self.approved_date = timezone.now()
        elif self.status == 'rejected' and not self.rejected_date:
            self.rejected_date = timezone.now()

        super().save(*args, **kwargs)