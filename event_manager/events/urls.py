from django.urls import path
from . import views


app_name = 'events'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about/', views.about, name='about'),
]