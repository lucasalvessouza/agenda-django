from django.contrib import admin
from .models import Contact, Category


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'last_name',
        'phone', 'email', 'created_at',
        'category', 'show'
    )
    list_display_links = ('id', 'name', 'last_name')
    list_per_page = 10
    search_fields = ('name', 'last_name', 'phone')
    list_editable = ('phone', 'show')


admin.site.register(Contact, ContactAdmin)
admin.site.register(Category)
