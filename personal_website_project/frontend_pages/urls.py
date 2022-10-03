from django.urls import path

from . import views

urlpatterns = [
    path("resume/", views.resume, name="resume"),
    path("", views.landing, name="home"),
    path("await/", views.await_admin, name="await_admin"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact_request, name="contact_request"),
    path("cookie-policy/", views.cookie_policy, name="cookie_policy"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-and-conditions/", views.terms_conditions, name="terms_conditions"),

]

