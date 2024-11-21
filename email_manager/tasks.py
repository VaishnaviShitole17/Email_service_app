import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from celery import shared_task
from django.conf import settings
from .models import EmailData

@shared_task
def send_email_task(email_id):
    email_data = EmailData.objects.get(id=email_id)
    subject = f"Special offer for {email_data.company_name}"
    message = f"Hello {email_data.company_name}, check out our products!"
    recipient = email_data.email

    # Create SendGrid client
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = Email('your_email@example.com')
    to_email = To(recipient)
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    # Send email
    response = sg.send(mail)

    # Save response details for tracking
    if response.status_code == 202:
        email_data.status = "Sent"
    else:
        email_data.status = "Failed"
    
    email_data.save()

    # You can log the response details for debugging
    print(f"Email sent to {recipient} with status {response.status_code}")
    return response.status_code
