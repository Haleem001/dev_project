# filters.py

import django_filters
from .models import AdoptionRequest

class AdoptionRequestFilter(django_filters.FilterSet):
    

    class Meta:
        model = AdoptionRequest
        fields = ['status']
