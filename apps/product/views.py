from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, DetailView, UpdateView

from apps.product.forms import *
from apps.product.models import *
from apps.service.models import Service, Field


class CreateCategory(CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'product/create_category.html'
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        return context


class ShowCategoryListAdmin(ListView, FormView):
    model = Category
    template_name = 'product/show_category_list_admin.html'

    success_url = reverse_lazy('product:show_categories_list_admin')
    form_class = CategoryListAdminForm

    def form_valid(self, form):
        category = Category.objects.get(id=form.cleaned_data['category_id'], is_active=True)
        category.is_active = False
        category.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['category_list'] = Category.objects.filter(is_active=True).order_by('id')
        return context


class UpdateCategory(UpdateView):
    model = Category
    template_name = 'product/update_category.html'
    success_url = reverse_lazy('product:show_categories_list_admin')
    form_class = CreateCategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        return context


class ChooseCategory(ListView):
    model = Category
    template_name = 'product/choose_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
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
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
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
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        category = self.kwargs['category']
        context['category_id'] = category
        if str(category) == '0':
            context['products'] = reversed(Product.objects.filter(is_active=True, category__is_active=True))
        else:
            try:
                category_object = Category.objects.get(id=category, is_active=True)
                if category_object:
                    context['products'] = Product.objects.filter(category=category_object, is_active=True)
            except:
                context['products'] = []
        return context

    def form_valid(self, form):
        keyword = form.cleaned_data['product']
        self.success_url = reverse_lazy('product:product_search_result', kwargs={'keyword': keyword})
        return super(ProductList, self).form_valid(form)


class ProductListAdmin(FormView):
    template_name = 'product/product_list_admin.html'
    success_url = reverse_lazy('product:product_search_result_admin',
                               kwargs={'keyword': ''})
    form_class = ProductListAdminForm

    def get_context_data(self, **kwargs):
        context = super(ProductListAdmin, self).get_context_data()
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        category = self.kwargs['category']
        context['category_id'] = category
        if str(category) == '0':
            context['products'] = reversed(Product.objects.filter(is_active=True, category__is_active=True))
        else:
            try:
                category_object = Category.objects.get(id=category, is_active=True)
                if category_object:
                    context['products'] = Product.objects.filter(category=category_object, is_active=True)
            except:
                context['products'] = []
        return context

    def form_valid(self, form):
        keyword = form.cleaned_data['product']
        deleted = form.cleaned_data['product_id']
        if str(deleted) != '-1':
            product = Product.objects.get(id=deleted, is_active=True, category__is_active=True)
            product.is_active = False
            product.save()
            self.success_url = reverse_lazy('product:product_list_admin', kwargs={'category': '0'})
        else:
            self.success_url = reverse_lazy('product:product_search_result_admin', kwargs={'keyword': keyword})
        return super(ProductListAdmin, self).form_valid(form)


class ProductSearchResult(ListView, FormView):
    model = Product
    template_name = 'product/product_list.html'
    success_url = reverse_lazy('product:product_search_result',
                               kwargs={'keyword': ''})
    form_class = SearchProductForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductSearchResult, self).get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        keyword = self.kwargs['keyword']
        context['keyword'] = keyword
        products = Product.objects.filter(is_active=True, category__is_active=True)
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


class ProductSearchResultAdmin(FormView):
    template_name = 'product/product_list_admin.html'
    success_url = reverse_lazy('product:product_search_result_admin',
                               kwargs={'keyword': ''})
    form_class = ProductListAdminForm

    def get_context_data(self, **kwargs):
        context = super(ProductSearchResultAdmin, self).get_context_data()
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        keyword = self.kwargs['keyword']
        context['keyword'] = keyword
        products = Product.objects.filter(is_active=True, category__is_active=True)
        searched_products = []
        for product in products:
            if keyword in product.name:
                searched_products.append(product)
        context['products'] = searched_products
        return context

    def form_valid(self, form):
        keyword = form.cleaned_data['product']
        deleted = form.cleaned_data['product_id']
        if str(deleted) != '-1':
            product = Product.objects.get(id=deleted, is_active=True, category__is_active=True)
            product.is_active = False
            product.save()
            self.success_url = reverse_lazy('product:product_list_admin', kwargs={'category': '0'})
        else:
            self.success_url = reverse_lazy('product:product_search_result_admin', kwargs={'keyword': keyword})
        return super(ProductSearchResultAdmin, self).form_valid(form)


class ProductDetails(DetailView):
    model = Product
    template_name = 'product/product_details.html'

    def dispatch(self, request, *args, **kwargs):
        if not Product.objects.filter(id=self.kwargs['pk'], is_active=True, category__is_active=True):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.filter(id=self.kwargs['pk'], is_active=True, category__is_active=True)
        if product:
            products = Product.objects.filter(category=product[0].category, is_active=True,
                                              category__is_active=True).exclude(name=product[0].name)
            if len(products) > 4:
                products = products[:4]
            context['related_products'] = products
        else:
            context['related_products'] = []
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        return context


class UpdateProduct(UpdateView):
    model = Product
    template_name = 'product/create_product.html'
    success_url = reverse_lazy('product:product_list_admin', kwargs={'category': '0'})
    form_class = CreateProductForm

    def dispatch(self, request, *args, **kwargs):
        if not Product.objects.filter(id=self.kwargs['pk'], is_active=True, category__is_active=True):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        return context
