from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from campaigns.models import Campaign, CampaignLog
from templates_app.models import EmailTemplate
from contacts.models import ContactList
from .forms import TemplateForm, ContactUploadForm, CampaignForm
from contacts.utils import parse_and_save_contacts

@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        campaigns = Campaign.objects.all().order_by('-created_at')
        logs = CampaignLog.objects.all()
    else:
        campaigns = Campaign.objects.filter(created_by=request.user).order_by('-created_at')
        logs = CampaignLog.objects.filter(campaign__created_by=request.user)

    total_campaigns = campaigns.count()
    total_sent = logs.filter(status='SUCCESS').count()
    total_failed = logs.filter(status='FAILED').count()
    recent_campaigns = campaigns[:10]

    context = {
        'total_campaigns': total_campaigns,
        'total_sent': total_sent,
        'total_failed': total_failed,
        'recent_campaigns': recent_campaigns
    }
    return render(request, 'dashboard.html', context)

@login_required
def template_list(request):
    templates = EmailTemplate.objects.all().order_by('-created_at')
    return render(request, 'template_list.html', {'templates': templates})

@login_required
def template_create(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Template created successfully.')
            return redirect('template_list')
    else:
        form = TemplateForm()
    return render(request, 'template_create.html', {'form': form})

@login_required
def contact_list_view(request):
    lists = ContactList.objects.all().order_by('-created_at')
    return render(request, 'contact_lists.html', {'lists': lists})

@login_required
def contact_upload(request):
    if request.method == 'POST':
        form = ContactUploadForm(request.POST, request.FILES)
        if form.is_valid():
            clist = ContactList.objects.create(name=form.cleaned_data['list_name'])
            mapping = {
                'email': form.cleaned_data['col_email'],
                'first_name': form.cleaned_data['col_first_name'],
                'last_name': form.cleaned_data['col_last_name'],
                'phone': form.cleaned_data['col_phone']
            }
            try:
                count = parse_and_save_contacts(request.FILES['file'], clist.id, mapping)
                messages.success(request, f'Successfully uploaded list with {count} contacts.')
                return redirect('contact_lists')
            except Exception as e:
                clist.delete()
                messages.error(request, f"Error parsing file: {str(e)}")
    else:
        form = ContactUploadForm()
    return render(request, 'contact_upload.html', {'form': form})

@login_required
def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.created_by = request.user
            campaign.save()
            messages.success(request, 'Campaign created! (Actual email sending is paused until Google Service Account is configured)')
            return redirect('dashboard')
    else:
        form = CampaignForm()
    return render(request, 'campaign_create.html', {'form': form})
