from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from events import views
from rest_framework import routers
from rest_framework.authtoken import views as drf_views
from .views import EventViewSet, ReviewViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Event API",
        default_version='v1',
        description="API для управления мероприятиями и отзывами",
    ),
        public=True,
        permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'api/reviews', ReviewViewSet)
router.register(r'api/events', views.EventViewSet)

events_router = routers.NestedDefaultRouter(router, r'api/events', lookup='event')
events_router.register(r'reviews', ReviewViewSet, basename='eventreviews')

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
] + router.urls + events_router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
    
urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='events/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='events/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='events/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='events/password_reset_complete.html'), name='password_reset_complete'),
    
]

urlpatterns += [
    path('api-token-auth/', drf_views.obtain_auth_token, name='api_token_auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]