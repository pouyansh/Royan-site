from django.shortcuts import render


def register(request):
    return render(request, "temporary/register.html")


def submit_primer_1(request):
    request.session['django_language'] = 'en'
    return render(request, "temporary/submit_primer_1.html")


def submit_primer_4(request):
    return render(request, "temporary/submit_primer_4.html")


def service_description(request):
    return render(request, "temporary/service_description.html")


def index(request):
    return render(request, "temporary/index.html")


def user_profile(request):
    return render(request, "temporary/user_profile.html")
