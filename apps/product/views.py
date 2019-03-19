from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.product.forms import *
from apps.product.models import *


class CreateCategory(CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'product/create_category.html'
    success_url = reverse_lazy('index:index')


class CreateProduct(CreateView):
    model = Product
    success_url = reverse_lazy('index:index')
