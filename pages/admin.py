from django.contrib import admin
from .models import Team, ContactMessage
from django.utils.html import format_html

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))

    thumbnail.short_description = 'Photo'

    list_display = ('id', 'thumbnail', 'first_name', 'designation', 'created_date')
    list_display_links = ('id', 'thumbnail', 'first_name',)
    search_fields = ('first_name', 'last_name', 'designation')
    list_filter = ('designation',)

# ContactMessage Admin Configuration
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'phone', 'sent_at')  # Fields to show in the list view
    list_display_links = ('id', 'name')  # Fields that are clickable to view the details
    search_fields = ('name', 'email', 'subject')  # Enable search by name, email, and subject
    list_filter = ('sent_at',)  # Enable filtering by the sent_at field (date/time)


admin.site.register(Team, TeamAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)

