from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.product.views import *

urlpatterns = [
    path('add_category/', staff_member_required(CreateCategory.as_view()), name='add_category'),
    path('category_list_admin/', staff_member_required(ShowCategoryListAdmin.as_view()),
         name='show_categories_list_admin'),
    url('update_category/(?P<pk>[0-9]+)/$', staff_member_required(UpdateCategory.as_view()), name='update_category'),
    url('add_product/(?P<pk>[0-9]+)/$', staff_member_required(CreateProduct.as_view()), name='add_product'),
    url(r'products/(?P<category>[0-9]+)/', ProductList.as_view(), name='product_list'),
    url(r'products_admin/(?P<category>[0-9]+)/', staff_member_required(ProductListAdmin.as_view()),
        name='product_list_admin'),
    url(r'search_products_result/(?P<keyword>\w+)/', ProductSearchResult.as_view(), name='product_search_result'),
    url(r'search_products_result_admin/(?P<keyword>\w+)/', staff_member_required(ProductSearchResultAdmin.as_view()),
        name='product_search_result_admin'),
    url('product_details/(?P<pk>[0-9]+)/$', ProductDetails.as_view(), name='product_details')
]