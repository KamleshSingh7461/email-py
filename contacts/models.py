from django.db import models

class ContactList(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    contact_list = models.ForeignKey(ContactList, related_name='contacts', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    extra_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
