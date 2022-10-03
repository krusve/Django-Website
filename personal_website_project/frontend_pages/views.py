from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string

from accounts.forms import ContactForm
from admin_data.models import PersonalInformation, Education, Extracurricular, Certificates, Work, Skills, \
    OtherSkill
import os


@login_required
def about(request):
    return render(request, "frontend_pages/about.html")

def landing(request):
    return render(request, "frontend_pages/landing.html")

def await_admin(request):
    return render(request, "frontend_pages/awaitAdmin.html")

def cookie_policy(request):
    return render(request, "frontend_pages/cookiePolicy.html")


def privacy_policy(request):
    return render(request, "frontend_pages/privacyPolicy.html")

def terms_conditions(request):
    return render(request, "frontend_pages/termsAndConditions.html")

@login_required
def resume(request):
    personal_information = PersonalInformation.objects.first()
    education = Education.objects.all().order_by('-end_date')
    extracurricular = Extracurricular.objects.all()
    certificates = Certificates.objects.all()
    work = Work.objects.all()
    new_list = {}
    x = list(Skills.objects.all().values_list('type', flat=True).distinct())

    for items in x:
        new_list[items] = Skills.objects.filter(type=items)

    other_skills = OtherSkill.objects.all()

    return render(request, "frontend_pages/resume.html", {"personal_information": personal_information,
                                                      "education": education,"extracurricular": extracurricular,
                                                            "certificates": certificates,
                                                            "work": work, "skills": new_list,
                                                            "other_skills": other_skills})
def contact_request(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form = contact_form.clean()

            subject_user = "Contact request received"
            subject_admin = "New Contact Request"

            contact_user = "accounts/contact_user.txt"
            contact_admin = "accounts/contact_admin.txt"

            c = {
                "user_email": contact_form['email_address'],
                'domain': settings.DOMAIN,
                'site_name': settings.SITE_NAME,
                'protocol': settings.PROTOCOL,
                'message': contact_form['message'],
                'name': contact_form['name'],
            }
            recipient_list = contact_form['email_address']

            email_user_message = render_to_string(contact_user, c)
            email_admin_message = render_to_string(contact_admin, c)

            try:
                send_mail(subject_user, email_user_message, settings.DEFAULT_FROM_EMAIL,
                          [recipient_list])
                # TODO: change email
                send_mail(subject_admin, email_admin_message, settings.DEFAULT_FROM_EMAIL,
                          ['recipient email'])
                messages.add_message(request, messages.SUCCESS, "Contact request successfully sent")
            except BadHeaderError:
                messages.add_message(request, messages.ERROR, "Something went wrong with that contact request!")
                return HttpResponse('Invalid header found.')
            return redirect('home')
    contact_form = ContactForm()
    return render(request, "frontend_pages/contactRequest.html", {"contact_form": contact_form})

