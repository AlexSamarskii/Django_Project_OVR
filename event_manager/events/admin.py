from django.contrib import admin
from .models import Category, Event, Registration, Review, Comment, Profile, Venue, Sponsor
    
@admin.action(description='Удалить выбранные мероприятия')
def delete_selected_events(modeladmin, request, queryset):
    queryset.delete()
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'category')
    search_fields = ('title', 'description')
    list_filter = ('category', 'date')
    
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity')
    search_fields = ('name', 'address')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Registration)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Sponsor)
admin.site.register(Event, EventAdmin)
admin.site.register(Category, CategoryAdmin)