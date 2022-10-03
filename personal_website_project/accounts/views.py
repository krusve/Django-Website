import threading

from django.conf import settings
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeDoneView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import RegisterForm, WebUserForm, ContactForm
from django.core.mail import EmailMessage

from admin_data.models import WebUser

def register_request(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        profile_form = WebUserForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            justification = str(profile_form.cleaned_data["justification"])

            user1 = user_form.save(commit=False)
            user1.is_active = False
            user1.save()

            profile = profile_form.save(commit=False)
            profile.user = user1
            profile.save()

            user1.save()

            subject = 'New User approval awaiting'
            message = justification
            # TODO: change recipient list
            recipient_list = 'admin@email.email'

            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_list],
                          fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.add_message(request, messages.SUCCESS, "Registration successful. Await admin approval.")
            return redirect("await_admin")
        else:
            messages.add_message(request, messages.ERROR, "Unsuccessful registration. Invalid information.")
    else:
        user_form = RegisterForm()
        profile_form = WebUserForm()
    return render(request, "accounts/register.html", {"user_form": user_form, "profile_form": profile_form,
                                                      "title": "Register"})

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject1 = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': settings.DOMAIN,
                        'site_name': settings.SITE_NAME,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': settings.PROTOCOL,
                    }

                    email1 = render_to_string(email_template_name, c)

                    try:
                        send_mail(subject1, email1, settings.DEFAULT_FROM_EMAIL, [user.email])
                        messages.add_message(request, messages.SUCCESS,
                                             "Password successfully reset")
                    except BadHeaderError:
                        messages.add_message(request, messages.ERROR, "Something went wrong...Try again or contact me")
                        return HttpResponse('Invalid header found.')

                    return redirect('done/')
    password_reset_form = PasswordResetForm()
    return render(request, "accounts/password_reset.html", {"password_reset_form": password_reset_form})

@login_required
def profile_request(request):
    user = request.user
    return render(request, "accounts/profile.html", {"user": user, "title": "Profile"})

@login_required
def delete_profile(request, pk):
    if request.method == "POST":
        query = get_object_or_404(User, pk=pk)
        web_user = get_object_or_404(WebUser, user=query)
        web_user.delete()
        query.delete()
        deletion_mail = "accounts/deletion_mail.txt"
        email_message = render_to_string(deletion_mail, {"user": query})
        # TODO: change email
        send_mail("User delete Account", email_message, settings.DEFAULT_FROM_EMAIL, ["recipient email"])
        messages.add_message(request, messages.SUCCESS, "Your Profile has been permanently deleted. Sorry to see you "
                                                        "go!")

    return redirect("home")


