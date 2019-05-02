from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.product.views import *

urlpatterns = [
    path('category/create', staff_member_required(CreateCategory.as_view()), name='add_category'),
    path('category/all/admin/', staff_member_required(ShowCategoryListAdmin.as_view()),
         name='show_categories_list_admin'),
    url('category/edit/(?P<pk>[0-9]+)/$', staff_member_required(UpdateCategory.as_view()),
        name='update_category'),
    path('category/choose/', staff_member_required(ChooseCategory.as_view()), name='choose_category'),
    url('product/create/(?P<pk>[0-9]+)/$', staff_member_required(CreateProduct.as_view()), name='add_product'),
    url('product/edit/(?P<pk>[0-9]+)/$', staff_member_required(UpdateProduct.as_view()), name='update_product'),
    url(r'product/all/(?P<category>[0-9]+)/', ProductList.as_view(), name='product_list'),
    url(r'product/all_admin/(?P<category>[0-9]+)/', staff_member_required(ProductListAdmin.as_view()),
        name='product_list_admin'),
    url(r'product/search_results/(?P<keyword>\w+)/', ProductSearchResult.as_view(), name='product_search_result'),
    url(r'product/search_results_admin/(?P<keyword>\w+)/', staff_member_required(ProductSearchResultAdmin.as_view()),
        name='product_search_result_admin'),
    url('product/details/(?P<pk>[0-9]+)/$', ProductDetails.as_view(), name='product_details')
]
