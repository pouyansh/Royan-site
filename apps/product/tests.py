from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.product.forms import ProductListAdminForm
from apps.product.models import *
from apps.product.views import ProductListAdmin, UpdateProduct


class Test(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client.login(username='admin', password='admin1234')
        category1 = Category.objects.create(name='test_category1', description='just a test category1')
        category2 = Category.objects.create(name='test_category2', description='just a test category2')
        image = SimpleUploadedFile(name='banner.jpg', content=open('./front/img/banner.jpg', 'rb').read(),
                                   content_type='image/jpeg')
        Product.objects.create(name='Product0', description='just a test product4', category=category2, image=image)
        Product.objects.create(name='Product1', description='just a test product1', category=category1, image=image)
        Product.objects.create(name='Product2', description='just a test product2', category=category1, image=image)
        Product.objects.create(name='Product3', description='just a test product3', category=category1, image=image)
        Product.objects.create(name='Product4', description='just a test product4', category=category1, image=image)

    # checks if index page shows correct products when multiple products are added
    def test_show_index(self):
        products = Product.objects.filter(is_active=True)
        product3 = products[len(products) - 2]
        product4 = products[len(products) - 1]

        response = self.client.get(reverse('index:index'))
        self.assertEqual(response.context['product1'], product4)
        self.assertEqual(response.context['product2'], product3)

    # checks if the new category would be shown in navbar or not
    def test_category(self):
        categories = Category.objects.filter(is_active=True)
        category1 = categories[len(categories) - 2]
        category2 = categories[len(categories) - 1]

        response = self.client.get(reverse('index:index'))
        self.assertEqual(category1 in response.context['product_categories'], True)
        self.assertEqual(category2 in response.context['product_categories'], True)

    # checks if the product details page displays product and related products correctly
    def test_related_products(self):
        products = Product.objects.filter(is_active=True)
        product0 = products[len(products) - 5]
        product1 = products[len(products) - 4]
        product2 = products[len(products) - 3]
        product3 = products[len(products) - 2]
        product4 = products[len(products) - 1]

        response = self.client.get(reverse('product:product_details', kwargs={'pk': product1.id}))
        self.assertEqual(response.context['object'], product1)
        related_products = response.context['related_products']
        self.assertEqual(False, product0 in related_products)
        self.assertEqual(False, product1 in related_products)
        self.assertEqual(True, product2 in related_products)
        self.assertEqual(True, product3 in related_products)
        self.assertEqual(True, product4 in related_products)

    # checks if search products work correctly
    def test_search_product(self):
        products = Product.objects.filter(is_active=True)
        product0 = products[len(products) - 5]
        product1 = products[len(products) - 4]
        product2 = products[len(products) - 3]
        product3 = products[len(products) - 2]
        product4 = products[len(products) - 1]
        form = ProductListAdminForm({'product': 'prod', 'product_id': -1})
        self.assertEqual(form.is_valid(), True)
        url = reverse('product:product_list_admin', kwargs={'category': 0})
        request = self.factory.post(url,
                                    data={'product': 'prod', 'product_id': -1})
        request.client = self.client
        response = ProductListAdmin.as_view()(request)
        response.client = self.client
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product:product_search_result_admin', kwargs={'keyword': 'prod'}))

        # response = self.client.get(reverse('product:product_search_result_admin', kwargs={'keyword': 'prod'})
        #                            , follow=True)
        # # request.user = self.client
        # # response = ProductSearchResult.as_view()(request)
        # # response.client = self.client
        # print(response.url)
        # products = response.context[-1]['products']
        # self.assertEqual(True, product0 in products)
        # self.assertEqual(True, product1 in products)
        # self.assertEqual(True, product2 in products)
        # self.assertEqual(True, product3 in products)
        # self.assertEqual(True, product4 in products)
        #
        # url = reverse('product:product_list_admin', kwargs={'category': 0})
        # request = self.factory.post(url,
        #                             data={'product': '1', 'product_id': -1})
        # response = ProductListAdmin.as_view()(request)
        # response.client = self.client
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.url, reverse('product:product_search_result_admin', kwargs={'keyword': '1'}))
        # response = self.client.get(reverse('product:product_search_result_admin', kwargs={'keyword': 'prod'}))
        # products = response.context['products']
        # self.assertEqual(False, product0 in products)
        # self.assertEqual(True, product1 in products)
        # self.assertEqual(False, product2 in products)
        # self.assertEqual(False, product3 in products)
        # self.assertEqual(False, product4 in products)

    # check if delete product works fine
    def test_delete_product(self):
        products = Product.objects.filter(is_active=True).order_by('id')
        product0 = products[len(products) - 5]
        product1 = products[len(products) - 4]
        product2 = products[len(products) - 3]
        product3 = products[len(products) - 2]
        product4 = products[len(products) - 1]

        url = reverse('product:product_list_admin', kwargs={'category': 0})
        request = self.factory.post(url,
                                    data={'product': 'prod', 'product_id': product0.id})
        ProductListAdmin.as_view()(request)
        products = Product.objects.filter(is_active=True)
        self.assertEqual(False, product0 in products)
        self.assertEqual(True, product1 in products)
        self.assertEqual(True, product2 in products)
        self.assertEqual(True, product3 in products)
        self.assertEqual(True, product4 in products)

        url = reverse('product:product_list_admin', kwargs={'category': 0})
        request = self.factory.post(url,
                                    data={'product': 'prod', 'product_id': product4.id})
        ProductListAdmin.as_view()(request)
        products = Product.objects.filter(is_active=True)
        self.assertEqual(False, product0 in products)
        self.assertEqual(True, product1 in products)
        self.assertEqual(True, product2 in products)
        self.assertEqual(True, product3 in products)
        self.assertEqual(False, product4 in products)
        response = self.client.get(reverse('index:index'))
        self.assertEqual(response.context['product1'], product3)
        self.assertEqual(response.context['product2'], product2)

    # checks if update product works well
    def test_update_product(self):
        products = Product.objects.filter(is_active=True)
        product2 = products[len(products) - 3]
        url = reverse('product:update_product', kwargs={'pk': product2.id})
        request = self.client.post(url,
                                   data={'name': 'prod2', 'description': 'edited!'})
        print(request)
        products = Product.objects.filter(is_active=True).order_by('id')
        product = products[len(products) - 3]
        self.assertEqual(product.name, 'prod2')
        self.assertEqual(product.description, 'edited!')
