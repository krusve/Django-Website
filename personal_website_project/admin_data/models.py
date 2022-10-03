import datetime

import django.utils.timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.utils import timezone


class WebUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    justification = models.TextField(max_length=300, help_text="Short justification for approving access",
                                     default="Want to get access", blank=False, null=True)

    def __str__(self):
        return self.justification


class PersonalInformation(models.Model):
    first_name = models.CharField(max_length=200,
                                  verbose_name='First Name')
    last_name = models.CharField(max_length=200, verbose_name='Last Name')
    street = models.CharField(max_length=200, default='Radilostraße 26')
    city = models.CharField(max_length=200, default='Frankfurt')
    zip_code = models.IntegerField(default='60489')
    country = models.CharField(max_length=100, default='Germany')
    phone_number = models.CharField(max_length=200,
                                    verbose_name='Phone Number')
    email = models.EmailField()
    birth_date = models.DateField(default="04/24/1998")
    description = models.CharField(max_length=300, help_text="Looking for a job? Short intro")
    about_me_text = models.TextField(max_length=600, help_text="Write a short introduction about yourself")
    title_name = models.CharField(max_length=50, help_text="Name to be displayed in Title e.g. Short version")
    title_text = models.TextField(max_length=500, help_text="Text to be displayed on title page")
    linkedIn_link = models.URLField(max_length=200)
    github_link = models.URLField(max_length=200)

    class Meta:
        verbose_name_plural = "Personal Information"

    def __str__(self):
        return '{} {} {} {}'.format(self.first_name, self.country,
                                    self.email, self.phone_number)


class Education(models.Model):
    type = models.CharField(max_length=100)
    gpa = models.DecimalField(max_digits=2, decimal_places=1, default=1.7)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    name = models.CharField(max_length=200)
    coursework = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name_plural = "Education"

    def __str__(self):
        return '{} {} {} {}'.format(self.name, self.type,
                                    self.description, self.start_date)


class Extracurricular(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    name = models.CharField(max_length=200)
    present = models.BooleanField(blank=True, help_text="Check if currently done")

    def __str__(self):
        return self.name


class Skills(models.Model):
    TYPES = [('Tools', 'Tool'), ('Development', 'Development'),
             ('Languages', 'Language'),
             ('Skills', 'Skill'), ('Programing Language', 'Programing Language')]
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=60, validators=[MaxValueValidator(100),
                                                        MinValueValidator(1)])
    type = models.CharField(max_length=50, choices=TYPES)

    def __str__(self):
        return self.name


class OtherSkill(models.Model):
    description = models.TextField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Certificates(models.Model):
    name = models.CharField(max_length=200)
    obtained_date = models.DateField()
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Certificates"

    def __str__(self):
        return self.name


class Work(models.Model):
    start_date = models.DateField(max_length=100)
    end_date = models.DateField(max_length=100, blank=True, default="10.10.2100")
    description = models.TextField()
    company = models.CharField(max_length=200)
    present = models.BooleanField(blank=True, help_text="Check if current occupation")
    role = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Work"

    def __str__(self):
        return self.company
