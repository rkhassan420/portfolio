import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):

    subject = 'ShowCraft — Your Verification Code'
    message = f"""
Hello,

Your ShowCraft OTP verification code is:

  {otp}

This code is valid for 5 minutes. Do not share it with anyone.

If you did not request this, please ignore this email.

— The ShowCraft Team
"""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
