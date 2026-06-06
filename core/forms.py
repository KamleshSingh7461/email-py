from django import forms
from campaigns.models import Campaign
from templates_app.models import EmailTemplate
from contacts.models import ContactList

class TemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'subject', 'body_html']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'subject': forms.TextInput(attrs={'class': 'form-input'}),
            'body_html': forms.Textarea(attrs={'class': 'form-input', 'rows': 15, 'style': 'font-family: monospace;'}),
        }

class ContactUploadForm(forms.Form):
    list_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-input'}))
    col_email = forms.CharField(max_length=255, initial='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    col_first_name = forms.CharField(max_length=255, initial='First Name', required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    col_last_name = forms.CharField(max_length=255, initial='Last Name', required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    col_phone = forms.CharField(max_length=255, initial='Phone', required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'contact_list', 'template']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_list': forms.Select(attrs={'class': 'form-input'}),
            'template': forms.Select(attrs={'class': 'form-input'}),
        }
