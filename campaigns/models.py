from django.db import models
from django.contrib.auth.models import User
from contacts.models import ContactList, Contact
from templates_app.models import EmailTemplate

class Campaign(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SCHEDULED', 'Scheduled'),
        ('SENDING', 'Sending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_list = models.ForeignKey(ContactList, on_delete=models.SET_NULL, null=True)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class CampaignLog(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='logs', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('SUCCESS', 'Success'), ('FAILED', 'Failed')))
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.campaign.name} -> {self.contact.email} [{self.status}]"
