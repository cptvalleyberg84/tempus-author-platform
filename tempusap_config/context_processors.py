from django.conf import settings


def google_form_url(request=None):
    return {
        'GOOGLE_FORM_URL': getattr(settings, 'GOOGLE_FORM_URL', '')
    }
