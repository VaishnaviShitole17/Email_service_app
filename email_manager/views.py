from django.shortcuts import render

def dashboard(request):
    return render(request, 'email_manager/dashboard.html')

import pandas as pd
from .models import EmailData

def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES['file']
        data = pd.read_csv(file)
        for _, row in data.iterrows():
            EmailData.objects.create(
                company_name=row['Company Name'],
                location=row['Location'],
                email=row['Email'],
                products=row.get('Products', '')
            )
    return render(request, 'upload_csv.html')

from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')



from django.shortcuts import render
from .forms import UploadCSVForm 
from django.http import HttpResponse

def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        # Handle the uploaded file here
        csv_file = request.FILES['csv_file']
        # Check if the file is a CSV
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Please upload a valid CSV file.", status=400)

        # Open the CSV file
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        # Loop through the CSV data and save it to the database
        for row in reader:
            # Extract data from CSV row
            company_name = row.get('Company Name')
            location = row.get('Location')
            email = row.get('Email')
            products = row.get('Products', '')  # Handle products column

            # Create an EmailData object for each row
            EmailData.objects.create(
                company_name=company_name,
                location=location,
                email=email,
                products=products
            )

        return HttpResponse("File uploaded successfully!")

    return render(request, 'email_manager/upload_csv.html')


from django.core.mail import send_mail
from .models import EmailData

def send_emails(request):
    emails = EmailData.objects.all()
    for email in emails:
        send_mail(
            'Subject',
            f'Hello {email.company_name}, check out our products!',
            'shitoletanishka@gmail.com',
            [email.email],
            fail_silently=False,
        )
    return render(request, 'email_sent.html')

import openai

openai.api_key = 'OpenAI_Key'

def generate_email_content(prompt, data):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt.format(**data),
        max_tokens=200,
    )
    return response['choices'][0]['text'].strip()


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import EmailData

@csrf_exempt
def email_status_webhook(request):
    if request.method == "POST":
        event_data = json.loads(request.body)
        for event in event_data:
            email_id = event.get("email")  # Assuming the email address is present
            status = event.get("event")    # Event like 'delivered', 'opened', etc.

            # Update the email status in your database
            try:
                email_data = EmailData.objects.get(email=email_id)
                email_data.delivery_status = status
                email_data.save()
            except EmailData.DoesNotExist:
                pass  # Handle missing email case if necessary

        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "failure"}, status=400)

from django.shortcuts import render
from .models import EmailData

def email_dashboard(request):
    emails = EmailData.objects.all()
    return render(request, 'email_dashboard.html', {'emails': emails})

# views.py
from django.http import JsonResponse
from .models import EmailStatus, EmailData
import json

def email_status_webhook(request):
    if request.method == "POST":
        payload = json.loads(request.body)
        
        for event in payload:
            email = event.get('email')
            event_type = event.get('event')  # e.g., delivered, bounced, opened
            email_data = EmailData.objects.filter(email=email).first()
            
            if email_data:
                status_obj, created = EmailStatus.objects.get_or_create(email_data=email_data, status=event_type)
                if event_type == 'delivered':
                    status_obj.delivery_status = 'Delivered'
                    status_obj.delivery_time = event.get('timestamp')  # Capture timestamp if available
                elif event_type == 'bounce':
                    status_obj.delivery_status = 'Bounced'
                    status_obj.failure_reason = event.get('reason', 'Unknown')
                elif event_type == 'open':
                    status_obj.opened = True
                else:
                    status_obj.status = 'Failed'

                status_obj.save()

        return JsonResponse({"status": "success"})
# views.py
from django.shortcuts import render
from .models import EmailData, EmailStatus

def dashboard(request):
    # Fetch email data and statuses
    emails = EmailData.objects.all()
    email_statuses = EmailStatus.objects.all()
    
    return render(request, 'dashboard.html', {
        'emails': emails,
        'email_statuses': email_statuses
    })
