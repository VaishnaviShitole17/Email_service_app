from django.db import models

class EmailData(models.Model):
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    email = models.EmailField()
    products = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name

class EmailStatus(models.Model):
    email_data = models.ForeignKey(EmailData, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # e.g., Sent, Scheduled, Failed
    delivery_status = models.CharField(max_length=50, null=True, blank=True)  # e.g., Delivered, Bounced
    opened = models.BooleanField(default=False)  # True if the email was opened by the recipient
    sent_time = models.DateTimeField(null=True, blank=True)  # Track when the email was sent
    delivery_time = models.DateTimeField(null=True, blank=True)  # Track when the email was delivered (if available)
    failure_reason = models.TextField(null=True, blank=True)  # Optional, for failure reasons

    def __str__(self):
        return f"{self.email_data.company_name} - {self.status}"

class Schedule(models.Model):
    email_data = models.ForeignKey(EmailData, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Schedule for {self.email_data.company_name} at {self.scheduled_time}"

