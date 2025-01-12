from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from events import views
from rest_framework import routers
from rest_framework.authtoken import views as drf_views

router = routers.DefaultRouter()
router.register(r'api/events', views.EventViewSet)

app_name = 'events'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about/', views.about, name='about'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete_event'),
    path('events/export/csv/', views.export_events_csv, name='export_events_csv'),
    path('captcha/', include('captcha.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/events/', views.api_event_list, name='api_event_list'),
    path('api/events/<int:pk>/', views.api_event_detail,
    name='api_event_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
    
urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='events/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='events/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='events/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='events/password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns += router.urls

urlpatterns += [
    path('api-token-auth/', drf_views.obtain_auth_token, name='api_token_auth'),
]