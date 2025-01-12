from django import forms
from .models import Event, Review
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


PROFANITY_WORDS = ['aaaaa', 'bbbbb', 'ccccc']

def validate_no_profanity(value):
    for bad_word in PROFANITY_WORDS:
        if re.search(r'\b' + re.escape(bad_word) + r'\b', value, re.IGNORECASE):
            raise ValidationError('Ваш комментарий содержит недопустимые слова.')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True,
    help_text='Обязательное поле. Введите действительный адрес электронной почты.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email


class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'category', 'main_image', 'document']
        widgets = {
        'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class ReviewForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty")
    
    comment = forms.CharField(
        widget=forms.Textarea,
        validators=[validate_no_profanity],
        max_length=500,
        label='Комментарий'
    )
    class Meta:
        model = Review
        fields = ['name', 'email', 'rating', 'comment']
        widgets = {
        'rating': forms.Select(choices=[(i, i) for i in range(1,
        6)]),
        }
        
    
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Review.objects.filter(event=self.event, email=email).exists():
            raise forms.ValidationError('Вы уже оставляли отзыв для этого мероприятия.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError('Пожалуйста, оставьте это поле пустым.')
        return cleaned_data