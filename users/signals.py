import threading

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from Conf import settings
from users.models import CustomUser, VerificationModel
from users.utils import get_random_code


def send_verification_email(email):
    try:
        code = get_random_code(email=email)
        VerificationModel.objects.create(code=code, user=CustomUser.objects.get(email=email))
        send_mail(
            subject='Verification email',
            message=f'Your code for last 2 minutes is {code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
    except Exception as e:
        print(e)

@receiver(post_save, sender=CustomUser)
def send_activate_code_signal(sender, instance, created, **kwargs):
    if created:
        email_thread = threading.Thread(target=send_verification_email, args=(instance.email,))
        email_thread.start()
