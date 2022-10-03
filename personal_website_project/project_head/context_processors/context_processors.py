from admin_data.models import PersonalInformation
from django.conf import settings


def links_footer(request):
    try:
        object = PersonalInformation.objects.first()
    finally:
        linkedIn = 'https://www.linkedin.com'
        github = 'https://www.github.com'
        email = settings.DEFAULT_FROM_EMAIL

    if object is not None:
        if object.linkedIn_link is not None:
            linkedIn = object.linkedIn_link
        else:
            linkedIn = 'https://www.linkedin.com'

        if object.github_link is not None:
            github = object.github_link
        else:
            github = 'https://www.github.com'

        if object.email is not None:
            email = object.email
        else:
            email = settings.DEFAULT_FROM_EMAIL
    else:
        linkedIn = 'https://www.linkedin.com'
        github = 'https://www.github.com'
        email = settings.DEFAULT_FROM_EMAIL


    return {
        'personal_obj_linkedin': linkedIn,
        'personal_obj_github': github,
        'personal_obj_email': email
    }


def google_analytics(request):
    if settings.GOOGLE_ANALYTICS_KEY is not None and not '':
        return {
            'GA_KEY': settings.GOOGLE_ANALYTICS_KEY,
        }
    else:
        return {
            'GA_KEY': '0000000',
        }
