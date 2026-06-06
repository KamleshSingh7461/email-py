from django.contrib import admin
from .models import ContactList, Contact

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0

@admin.register(ContactList)
class ContactListAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [ContactInline]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'contact_list')
    list_filter = ('contact_list',)
    search_fields = ('email', 'first_name', 'last_name')
