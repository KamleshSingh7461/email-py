import base64
from email.message import EmailMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build
from .models import CampaignLog

def render_template(html_content, contact):
    """
    Replaces variables like $User or [PHONE NUMBER] with actual contact data.
    """
    rendered = html_content
    
    if contact.first_name:
        rendered = rendered.replace('$User', contact.first_name)
    else:
        rendered = rendered.replace('$User', 'there')
        
    if contact.phone_number:
        rendered = rendered.replace('[PHONE NUMBER]', contact.phone_number)
        
    for key, value in contact.extra_data.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
        
    return rendered

def get_gmail_service(service_account_file, delegate_email):
    """
    Authenticate using a Service Account with Domain-Wide Delegation.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    creds = creds.with_subject(delegate_email)
    service = build('gmail', 'v1', credentials=creds)
    return service

def send_campaign_emails(campaign, service_account_file, delegate_email):
    """
    Sends emails for a campaign and logs the status.
    """
    try:
        service = get_gmail_service(service_account_file, delegate_email)
    except Exception as e:
        campaign.status = 'FAILED'
        campaign.save()
        return False
        
    contacts = campaign.contact_list.contacts.all()
    template = campaign.template
    
    campaign.status = 'SENDING'
    campaign.save()
    
    for contact in contacts:
        rendered_body = render_template(template.body_html, contact)
        
        message = EmailMessage()
        message.set_content("Please view this email in an HTML compatible client.")
        message.add_alternative(rendered_body, subtype='html')
        
        message['To'] = contact.email
        message['From'] = delegate_email
        message['Subject'] = template.subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        
        try:
            sent_message = service.users().messages().send(userId='me', body=create_message).execute()
            CampaignLog.objects.create(
                campaign=campaign,
                contact=contact,
                status='SUCCESS'
            )
        except Exception as e:
            CampaignLog.objects.create(
                campaign=campaign,
                contact=contact,
                status='FAILED',
                error_message=str(e)
            )
            
    campaign.status = 'COMPLETED'
    campaign.save()
    return True
