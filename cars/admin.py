from django.contrib import admin
from .models import Car
from django.utils.html import format_html

# Register your models here.

class CarAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.car_photo.url))

    thumbnail.short_description = 'Car Image'
    list_display = ('id','thumbnail','car_title', 'city', 'color', 'model', 'year', 'body_style', 'fuel_type', 'is_featured')
    list_display_links = ('id', 'thumbnail', 'car_title')
    list_editable = ('is_featured',)
    search_fields = ('id', 'car_title', 'city', 'model', 'body_style','fuel_type')
    list_filter = ('city', 'model', 'body_style', 'fuel_type')
     
     # Add custom actions
    actions = ['approve_cars', 'reject_cars']

    def approve_cars(self, request, queryset):
        updated_count = queryset.update(status='Approved')  # Update status to 'Approved'
        self.message_user(request, f"{updated_count} car(s) successfully approved.")
    approve_cars.short_description = "Approve selected cars"

    def reject_cars(self, request, queryset):
        updated_count = queryset.update(status='Rejected')  # Update status to 'Rejected'
        self.message_user(request, f"{updated_count} car(s) successfully rejected.")
    reject_cars.short_description = "Reject selected cars"
admin.site.register(Car, CarAdmin)
