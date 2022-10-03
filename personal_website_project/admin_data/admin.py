from django.contrib import admin
from .models import PersonalInformation, Extracurricular, Education, Certificates, Work, Skills, OtherSkill, WebUser
from django.contrib.admin import ModelAdmin


# Register your models here.

class PersonalInformationAdmin(ModelAdmin):
    list_display = ('first_name', 'country', 'email', 'phone_number')


admin.site.register(PersonalInformation, PersonalInformationAdmin)
admin.site.register(Education)
admin.site.register(Extracurricular)
admin.site.register(Skills)
admin.site.register(OtherSkill)
admin.site.register(Certificates)
admin.site.register(Work)
admin.site.register(WebUser)
