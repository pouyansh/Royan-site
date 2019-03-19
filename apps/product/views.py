from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.product.models import *


class CreateProduct(CreateView):
    model = Product
    success_url = reverse_lazy('index:index')
