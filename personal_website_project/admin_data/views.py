import datetime

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .forms import PersonalInfForm, EducationForm, ExtracurricularForm, \
    CertificatesSkillsForm, WorkForm, SkillsForm, OtherSkillForm
from .models import PersonalInformation, Education, Extracurricular, Certificates, Work, Skills, \
    OtherSkill, WebUser
from django.contrib import messages
from django.conf.global_settings import EMAIL_HOST_USER


# ----------------------------------------------
#        BASIC FUNCTIONS
# ----------------------------------------------







@staff_member_required
def list_all_user(request):
    user_justification = WebUser.objects.all()
    return render(request, "admin_data/users.html", {"users": user_justification, "title": "List of Users"})

@staff_member_required
def mail_on_approval(user):
    subject = "Approval granted"
    email_template_name = "admin_data/approval_mail.txt"
    c = {
        "email": user.email,
        "domain": settings.DOMAIN,
        "site_name": settings.SITE_NAME,
        "username": user.username,
        'protocol': settings.PROTOCOL,
    }

    email_message = render_to_string(email_template_name, c)

    try:
        send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [user.email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return redirect("password_reset/done/")

@staff_member_required
def change_status(request, pk):
    if request.method == 'POST':
        query = get_object_or_404(WebUser, pk=pk)
        user = get_object_or_404(User, pk=query.user_id)
        if user.is_active:
            user.is_active = False
            user.save()
            HttpResponseRedirect('/admin_data/listUsers/')
        else:
            user.is_active = True
            user.save()


            email_template_name = "admin_data/approval_mail.txt"
            c = {
                "email": user.email,
                "domain": settings.DOMAIN,
                "site_name": settings.SITE_NAME,
                "username": user.username,
                'protocol': settings.PROTOCOL,
            }

            email_message = render_to_string(email_template_name, c)

            try:
                send_mail("Approval granted", email_message, settings.DEFAULT_FROM_EMAIL, [user.email])
                messages.add_message(request, messages.SUCCESS, "User " + str(user.email) + " has access now")

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect("/admin_data/listUsers/")
    return HttpResponseRedirect('/admin_data/listUsers/')


@staff_member_required
def curriculum_vitae_data(request):
    return render(request, "admin_data/curriculumVitaeData.html", {"title": "Curriculum Vitae Data"})


@staff_member_required
def create_personal_information(request):
    if PersonalInformation.objects.count() > 0:
        if PersonalInformation.objects.count() > 1:
            error_message = "Please contact your Admin, you seem have more than one personal information entries in " \
                            "your database "
            error_title = "Corrupt Data"
            messages.add_message(request, messages.ERROR, "More entries than allowed in database")

            return render(request, "main_app/errorPage.html",
                          {"errorMessage": error_message, "errorTitle": error_title})
        else:
            button_name = "Update"
            entry = PersonalInformation.objects.first()
            fields = PersonalInformation._meta.get_fields()

            initial_values = initial_values_creation(fields, entry)

            form = PersonalInfForm(initial=initial_values)

    else:
        button_name = 'Create'
        form = PersonalInfForm()

    if request.method == 'POST':
        if PersonalInformation.objects.count() > 0:
            entry = PersonalInformation.objects.first()
            fields = PersonalInformation._meta.get_fields()
            initial_values = initial_values_creation(fields, entry)

            form = PersonalInfForm(request.POST, initial=initial_values)
            id_num = entry.id

            if form.is_valid():
                new_entry = PersonalInformation.objects.filter(id=id_num)

                new_values = form_values_creation(fields, form, initial_values)

                new_entry.update(**new_values)

                messages.add_message(request, messages.SUCCESS, "Entry Updated")

                return redirect('curriculumVitaeData')
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong")


        else:
            # if PersonalInformation.objects.count() > 0:

            form = PersonalInfForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Entry Created")

                return redirect('curriculumVitaeData')

    return render(request, "admin_data/createPersonalInformation.html",
                  {"form": form, "buttonName": button_name, "title": "Personal Information"})


# ----------------------------------------------
#        EDUCATION
# ----------------------------------------------
@staff_member_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Education added")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong")

    else:
        form = EducationForm()

    return render(request, "admin_data/addEducation.html", {"form": form, "title": "Add Education"})


@staff_member_required
def edit_education(request, pk):
    fields = Education._meta.get_fields()

    if request.method == 'POST':
        form = EducationForm(request.POST)
        entry = Education.objects.filter(id=pk).first()
        initial_values = initial_values_creation(fields, entry)

        if form.is_valid():
            entry_update = Education.objects.filter(id=pk)
            new_values = form_values_creation(fields, form, initial_values)

            entry_update.update(**new_values)
            messages.add_message(request, messages.SUCCESS, "Education updated")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong")

    else:
        entry = Education.objects.filter(id=pk).first()
        initial_values = initial_values_creation(fields, entry)
        form = EducationForm(initial=initial_values)

    return render(request, "admin_data/editEducation.html", {"form": form, "title": "Edit Education"})


@staff_member_required
def list_education(request):
    all_entries = Education.objects.all()
    return render(request, "admin_data/listEducation.html",
                  {"all_entries": all_entries, "title": "List of Education"})


@staff_member_required
@require_POST
def delete_education(request, pk):
    if request.method == 'POST':
        query = get_object_or_404(Education, pk=pk)
        query.delete()
    return redirect('curriculumVitaeData')


# ----------------------------------------------
#        Extracurricular
# ----------------------------------------------
@staff_member_required
def add_extracurricular(request):
    if request.method == 'POST':
        form = ExtracurricularForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Extracurricular added")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong")

    else:
        form = ExtracurricularForm()

    return render(request, "admin_data/addExtracurricular.html", {"form": form, "title": "Add Extracurriculars"})


@staff_member_required
def list_extracurricular(request):
    all_entries = Extracurricular.objects.all()
    return render(request, "admin_data/listExtracurricular.html",
                  {"all_entries": all_entries, "title": "List of Extracurriculars"})


@staff_member_required
def edit_extracurricular(request, pk):
    fields = Extracurricular._meta.get_fields()
    if request.method == 'POST':
        form = ExtracurricularForm(request.POST)
        entry = get_object_or_404(Extracurricular, pk=pk)

        initial_values = initial_values_creation(fields, entry)

        if form.is_valid():
            entry_update = Extracurricular.objects.filter(id=pk)
            new_values = form_values_creation(fields, form, initial_values)
            entry_update.update(**new_values)
            messages.add_message(request, messages.SUCCESS, "Entry updated")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong!")


    else:
        entry = Extracurricular.objects.filter(id=pk).first()
        initial_values = initial_values_creation(fields, entry)
        form = ExtracurricularForm(initial=initial_values)

    return render(request, "admin_data/editExtracurricular.html",
                  {"form": form, "title": "Edit Extracurriculars"})


@staff_member_required
@require_POST
def delete_extracurricular(request, pk):
    if request.method == 'POST':
        query = get_object_or_404(Extracurricular, pk=pk)
        query.delete()
    return redirect('curriculumVitaeData')


# ----------------------------------------------
#        IT SKILLS
# ----------------------------------------------
@staff_member_required
def add_other_skill(request):
    if request.method == 'POST':
        form = OtherSkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Skill added")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong")


    else:
        form = OtherSkillForm()

    return render(request, "admin_data/addOtherSkill.html", {"form": form, "title": "Add other Skill"})


@staff_member_required
def list_other_skill(request):
    all_entries = OtherSkill.objects.all()
    return render(request, "admin_data/listOtherSkill.html", {"all_entries": all_entries,
                                                                    "title": "List of "
                                                                             "Skills"})


@staff_member_required
def edit_other_skill(request, pk):
    fields = OtherSkill._meta.get_fields()

    if request.method == 'POST':
        form = OtherSkillForm(request.POST)
        entry = get_object_or_404(OtherSkill, pk=pk)

        initial_values = initial_values_creation(fields, entry)

        if form.is_valid():
            entry_update = OtherSkill.objects.filter(id=pk)
            new_values = form_values_creation(fields, form, initial_values)
            entry_update.update(**new_values)
            messages.add_message(request, messages.SUCCESS, "Entry updated")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong")

    else:
        entry = OtherSkill.objects.filter(id=pk).first()
        initial_values = initial_values_creation(fields, entry)
        form = OtherSkillForm(initial=initial_values)

    return render(request, "admin_data/editOtherSkill.html", {"form": form, "title": "Edit other Skill"})


@staff_member_required
@require_POST
def delete_other_skill(request, pk):
    if request.method == 'POST':
        query = get_object_or_404(OtherSkill, pk=pk)
        query.delete()
    return redirect('curriculumVitaeData')


# ----------------------------------------------
#        Certificates
# ----------------------------------------------
@staff_member_required
def add_cert(request):
    if request.method == 'POST':
        form = CertificatesSkillsForm(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Certificate added")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong when adding Certificate")


    else:
        form = CertificatesSkillsForm()

    return render(request, "admin_data/addCertSkill.html", {"form": form, "title": "Add Certificate"})

@staff_member_required
def list_cert(request):
    all_entries = Certificates.objects.all()
    return render(request, "admin_data/listCertSkill.html",
                  {"all_entries": all_entries, "title": "List of Certificates"})


@staff_member_required
def edit_cert(request, pk):
    fields = Certificates._meta.get_fields()

    if request.method == 'POST':
        form = CertificatesSkillsForm(request.POST)
        entry = get_object_or_404(Certificates, pk=pk)

        initial_values = initial_values_creation(fields, entry)
        if form.is_valid():
            entry_update = Certificates.objects.filter(id=pk)
            new_values = form_values_creation(fields, form, initial_values)
            entry_update.update(**new_values)
            messages.add_message(request, messages.SUCCESS, "Certificate updated")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Updating Certificate went wrong")


    else:
        entry = Certificates.objects.filter(id=pk).first()
        initial_values = initial_values_creation(fields, entry)
        form = CertificatesSkillsForm(initial=initial_values)

    return render(request, "admin_data/editCertSkill.html", {"form": form, "title": "Edit Certificate"})


@staff_member_required
@require_POST
def delete_cert(request, pk):
    if request.method == 'POST':
        query = get_object_or_404(Certificates, pk=pk)
        query.delete()
    return redirect('curriculumVitaeData')


# ----------------------------------------------
#        WORK
# ----------------------------------------------
@staff_member_required
def add_work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Work added")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Adding work went wrong")

    else:
        form = WorkForm()

    return render(request, "admin_data/addWork.html", {"form": form, "title": "Add Work"})


@staff_member_required
def list_work(request):
    all_entries = Work.objects.all()
    return render(request, "admin_data/listWork.html", {"all_entries": all_entries, "title": "List of Work"})


@staff_member_required
def edit_work(request, pk):
    fields = Work._meta.get_fields()

    if request.method == 'POST':
        form = WorkForm(request.POST)
        entry = get_object_or_404(Work, pk=pk)

        initial_values = initial_values_creation(fields, entry)

        if form.is_valid():
            entry_update = Work.objects.filter(id=pk)
            new_values = form_values_creation(fields, form, initial_values)
            entry_update.update(**new_values)
            messages.add_message(request, messages.SUCCESS, "Work updated")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Updating work went wrong")

    else:
        entry = Work.objects.filter(id=pk).first()
        initial_values = initial_values_creation(fields, entry)
        form = WorkForm(initial=initial_values)

    return render(request, "admin_data/editWork.html", {"form": form, "title": "Edit Work"})


@staff_member_required
@require_POST
def delete_work(request, pk):
    if request.method == 'POST':
        query = get_object_or_404(Work, pk=pk)
        query.delete()
    return redirect('curriculumVitaeData')


# ----------------------------------------------
#        Skill FUNCTIONS
# ----------------------------------------------
@staff_member_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Skill added")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Adding Skill went wrong")

    else:
        form = SkillsForm()

    return render(request, "admin_data/addSkill.html", {"form": form, "title": "Add Skill"})


@staff_member_required
def list_skill(request):
    all_entries = Skills.objects.all()
    return render(request, "admin_data/listSkill.html", {"all_entries": all_entries,
                                                               "title": "List of "
                                                                        "Skills"})


@staff_member_required
def edit_skill(request, pk):
    fields = Skills._meta.get_fields()

    if request.method == 'POST':
        form = SkillsForm(request.POST)
        entry = get_object_or_404(Skills, pk=pk)
        initial_values = initial_values_creation(fields, entry)

        if form.is_valid():
            entry_update = Skills.objects.filter(id=pk)
            new_values = form_values_creation(fields, form, initial_values)
            entry_update.update(**new_values)
            messages.add_message(request, messages.SUCCESS, "Skill updated")
            return redirect('curriculumVitaeData')
        else:
            messages.add_message(request, messages.ERROR, "Skill update went wrong")

    else:
        entry = Skills.objects.filter(id=pk).first()
        initial_values = initial_values_creation(fields, entry)
        form = SkillsForm(initial=initial_values)

    return render(request, "admin_data/editSkill.html", {"form": form, "title": "Edit Skill"})


@staff_member_required
@require_POST
def delete_skill(request, pk):
    if request.method == 'POST':
        query = get_object_or_404(Skills, pk=pk)
        query.delete()
    return redirect('curriculumVitaeData')



# ----------------------------------------------
#        UTILITY FUNCTIONS
# ----------------------------------------------
def initial_values_creation(fields, entry):
    """ Utility function to return array of initial values (database values) from previous entries """

    initial_values = {}
    for field in fields:
        if field.name == "id":
            pass
        else:
            initial_values[field.name] = getattr(entry, field.name)

    return initial_values


def form_values_creation(fields, form, initial_values):
    """Comparison function of user input with previous values to determine what fields to update"""
    new_values = {}
    form_clean = form.cleaned_data

    for field in fields:
        if field.name == "id":
            pass
        elif form_clean[field.name] != initial_values[field.name]:
            new_values[field.name] = form_clean[field.name]

    return new_values
