from django.shortcuts import render


def register(request):
    return render(request, "temporary/register.html")


def submit_primer_1(request):
    return render(request, "temporary/submit_primer_1.html")


def submit_primer_2(request):
    return render(request, "temporary/submit_primer_2.html")


def service_description(request):
    return render(request, "temporary/service_description.html")
