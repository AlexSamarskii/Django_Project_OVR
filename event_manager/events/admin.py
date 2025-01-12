from django.contrib import admin
from .models import Category, Event, Registration, Review, Comment, Profile, Venue, Sponsor
from django.utils.html import format_html
    
@admin.action(description='Удалить выбранные мероприятия')
def delete_selected_events(modeladmin, request, queryset):
    queryset.delete()
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'category',
    'display_image')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description')
    ordering = ('date',)
    readonly_fields = ('display_image_preview',)
    fieldsets = ((None, {
    'fields': ('title', 'description', 'date', 'location',
    'category')
    }),
    ('Media', {
    'fields': ('main_image', 'display_image_preview',
    'document')
    }),)
    
    
    def display_image(self, obj):
        if obj.main_image:
            return 'Да'
        return 'Нет'

    display_image.short_description = 'Изображение'
    
    def display_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height:200px;"/>', obj.main_image.url)
        return 'Нет изображения'
    display_image_preview.short_description = 'Предпросмотр изображения'
    
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