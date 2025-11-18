
# hospitals/utils.py
import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import HospitalAdmin, Hospital
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


def get_or_create_admin_user(email: str, password: str):
    """
    Creates or fetches an admin user. Works with both username-based and email-based custom users.
    - If your custom User uses USERNAME_FIELD='email', we look up by email.
    - If it uses 'username', we set username=email for convenience.
    """
    defaults = {
        'email': email,
        'is_staff': True,
        'is_superuser': False,
    }

    # Decide lookup based on the model's USERNAME_FIELD
    username_field = getattr(User, 'USERNAME_FIELD', 'username')
    if username_field == 'email':
        lookup = {'email': email}
    else:
        # For username-based models, we use email as the username string
        lookup = {'username': email}
        defaults['username'] = email

    user, _created = User.objects.get_or_create(**lookup, defaults=defaults)
    user.set_password(password)
    user.save()
    return user


def approve_hospital_and_notify(hospital: Hospital):
    """
    Approves the given hospital (caller should set status and save),
    creates/links a HospitalAdmin, and sends credentials via email.
    """
    print("🚀 approve_hospital_and_notify() called for:", hospital.email)

    # Generate a fresh password every approval
    password = secrets.token_urlsafe(10)

    # Create/update admin user
    user = get_or_create_admin_user(hospital.email, password)

    # Link HospitalAdmin
    HospitalAdmin.objects.update_or_create(hospital=hospital, defaults={'user': user})

    # Send email
    logger.info("📤 Preparing to send email...")
    print("From:", settings.DEFAULT_FROM_EMAIL)
    print("To:", hospital.email)
    try:
        send_mail(
            subject='Hospital Approved - Admin Credentials',
            message=(
                f'Dear {hospital.name},\n\n'
                f'Your hospital has been approved.\n\n'
                f'Login: http://localhost:8000/admin/\n'
                f'Username: {hospital.email}\n'
                f'Password: {password}\n\n'
                f'Please change your password after first login.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[hospital.email],
            fail_silently=False,
        )
        logger.info(f"🚀 approve_hospital_and_notify() called for: {hospital.email}")
    except Exception as e:
        logger.error(f"❌ Email failed: {e}")
        # No re-raise to avoid breaking admin flow; API will return message separately.
