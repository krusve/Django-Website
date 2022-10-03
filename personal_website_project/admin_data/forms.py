from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput
from .models import PersonalInformation, Education, Extracurricular, Certificates, Work, Skills, \
    OtherSkill, WebUser
from django.contrib.admin import ModelAdmin

from django.conf import settings





class PersonalInfForm(ModelForm):
    class Meta:
        model = PersonalInformation
        fields = "__all__"
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
        }


class EducationForm(ModelForm):
    type = forms.CharField()
    gpa = forms.DecimalField()
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.TextInput()
    name = forms.CharField()
    coursework = forms.CharField()

    class Meta:
        model = Education
        fields = ('type', 'gpa', 'start_date', 'end_date', 'description', 'name', 'coursework')
        # widgets = {
        #     'start_date': DateInput(attrs={'type': 'date'}),
        #     'end_date': DateInput(attrs={'type': 'date'}),
        # }


class ExtracurricularForm(ModelForm):
    def clean(self):
        cleaned_data = super(ExtracurricularForm, self).clean()
        if not cleaned_data.get('present') and not cleaned_data.get('end_date'):  # This will check for None or Empty
            raise ValidationError({'end_date': 'One of Present OR End-date should have a value.'})

    class Meta:
        model = Extracurricular
        fields = "__all__"
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


class OtherSkillForm(ModelForm):
    class Meta:
        model = OtherSkill
        fields = "__all__"
        verbose_name_plural = "OtherSkill"


class SkillsForm(ModelForm):
    class Meta:
        model = Skills
        fields = "__all__"
        verbose_name_plural = "Skills"


class CertificatesSkillsForm(ModelForm):
    class Meta:
        model = Certificates
        fields = "__all__"
        widgets = {
            'obtained_date': DateInput(attrs={'type': 'date'}),
        }
        verbose_name_plural = "Certificates"


class WorkForm(ModelForm):

    def clean(self):
        cleaned_data = super(WorkForm, self).clean()
        if not cleaned_data.get('present') and not cleaned_data.get('end_date'):  # This will check for None or Empty
            raise ValidationError({'end_date': 'One of Present OR End-date should have a value.'})

    class Meta:
        model = Work
        fields = "__all__"
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


