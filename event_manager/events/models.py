from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxLengthValidator
#from imagekit.models import ImageSpecField
# from imagekit.processors import ResizeToFill


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    
class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    capacity = models.IntegerField()
    def __str__(self):
        return self.name
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    location = models.CharField(max_length=200)
    main_image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    # main_image_thumbnail = ImageSpecField(
    #     source='main_image',
    #     processors=[ResizeToFill(100, 50)],
    #     format='JPEG',
    #     options={'quality': 60}
    #     )
    document = models.FileField(
        upload_to='event_documents/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf',
        'docx'])])
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('events:event_detail', args=[str(self.id)])
    
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
    related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user.username} зарегистрировался на {self.event.title}'
        
class Review(models.Model):
    event = models.ForeignKey('Event', related_name='reviews',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 254)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(validators=[MaxLengthValidator(500)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Review by {self.name} for {self.event.title}'
    
    
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
    related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Комментарий {self.user.username} к {self.event.title}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    subscribed = models.BooleanField(default=False)
    def __str__(self):
        return f'Профиль {self.user.username}'
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    print("Модели успешно созданы")
      
class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsors/', blank=True, null=True)
    website = models.URLField(blank=True)
    events = models.ManyToManyField(Event, related_name='sponsors', blank=True)
    def __str__(self):
        return self.name
    