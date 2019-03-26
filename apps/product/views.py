from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, DetailView

from apps.product.forms import *
from apps.product.models import *


class CreateCategory(CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'product/create_category.html'
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        return context


class ShowCategoryListAdmin(ListView, FormView):
    model = Category
    template_name = 'product/show_category_list_admin.html'

    success_url = reverse_lazy('product:show_categories_list_admin')
    form_class = CategoryListAdminForm

    def form_valid(self, form):
        Category.objects.filter(id=form.cleaned_data['category_id']).delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        return context


class CreateProduct(CreateView):
    model = Product
    success_url = reverse_lazy('index:index')
    form_class = CreateProductForm
    template_name = 'product/create_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = category
        kwargs['category'] = category
        print(category.name)
        context['product_categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        form.instance.category = category
        return super().form_valid(form)


class ProductList(ListView, FormView):
    model = Product
    template_name = 'product/product_list.html'
    success_url = reverse_lazy('product:product_search_result',
                               kwargs={'keyword': ''})
    form_class = SearchProductForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        category = self.kwargs['category']
        context['category_id'] = category
        if str(category) == '0':
            context['products'] = reversed(Product.objects.filter())
        else:
            try:
                category_object = Category.objects.get(id=category)
                if category_object:
                    context['products'] = Product.objects.filter(category=category_object)
            except:
                context['products'] = []
        return context

    def form_valid(self, form):
        keyword = form.cleaned_data['product']
        self.success_url = reverse_lazy('product:product_search_result', kwargs={'keyword': keyword})
        return super(ProductList, self).form_valid(form)


class ProductSearchResult(ListView, FormView):
    model = Product
    template_name = 'product/product_list.html'
    success_url = reverse_lazy('product:product_search_result',
                               kwargs={'keyword': ''})
    form_class = SearchProductForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductSearchResult, self).get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        keyword = self.kwargs['keyword']
        context['keyword'] = keyword
        products = Product.objects.all()
        searched_products = []
        for product in products:
            if keyword in product.name:
                searched_products.append(product)
        context['products'] = searched_products
        context['category_id'] = -1
        return context

    def form_valid(self, form):
        keyword = form.cleaned_data['product']
        self.success_url = reverse_lazy('product:product_search_result', kwargs={'keyword': keyword})
        return super(ProductSearchResult, self).form_valid(form)


class ProductDetails(DetailView):
    model = Product
    template_name = 'product/product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['product_categories'] = Category.objects.all()
        return context
