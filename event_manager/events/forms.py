from django import forms
from .models import Event, Review


class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'category', 'main_image', 'document']
        widgets = {
        'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['name', 'email', 'rating', 'comment']
        widgets = {
        'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }