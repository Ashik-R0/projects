from django import forms
from .models import Tourpakage

class TourPackageForm(forms.ModelForm):
    class Meta:
        model = Tourpakage
        fields = ['title', 'price', 'duration', 'location', 'start_date', 'end_date', 'image', 'description', 'trending']
