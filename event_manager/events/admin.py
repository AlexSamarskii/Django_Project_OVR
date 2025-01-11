from django.contrib import admin
from .models import Category, Event, Registration, Review, Comment, Profile, Venue, Sponsor

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category', 'venue')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
    
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity')
    search_fields = ('name', 'address')
    
admin.site.register(Registration)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Sponsor)