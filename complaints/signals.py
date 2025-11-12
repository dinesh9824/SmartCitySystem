from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Complaint


@receiver(post_save, sender=Complaint)
def send_complaint_notification(sender, instance, created, **kwargs):
    """Send email notification when a new complaint is created or status is updated"""
    if created:
        # New complaint created
        subject = f'New Complaint Submitted: {instance.title}'
        message = f'''
Dear {instance.user.first_name},

Your complaint has been successfully submitted to Smart City System.

Complaint Details:
- Title: {instance.title}
- Category: {instance.get_category_display()}
- Status: {instance.get_status_display()}
- Description: {instance.description}

Your complaint ID is: {instance.id}

We will review your complaint and update you on the progress.

Thank you for using Smart City System.

Best regards,
Smart City Administration
        '''
    else:
        # Status updated
        subject = f'Complaint Status Update: {instance.title}'
        message = f'''
Dear {instance.user.first_name},

Your complaint status has been updated.

Complaint Details:
- Title: {instance.title}
- Category: {instance.get_category_display()}
- New Status: {instance.get_status_display()}
- Description: {instance.description}

Thank you for using Smart City System.

Best regards,
Smart City Administration
        '''
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER or 'noreply@smartcity.com',
        [instance.user.email],
        fail_silently=False,
    )
