from django.views.generic import TemplateView

from apps.product.models import Category


class AdminPanel(TemplateView):
    template_name = 'royan_admin/admin_panel.html'

    def get_context_data(self, **kwargs):
        context = super(AdminPanel, self).get_context_data()
        context['product_categories'] = Category.objects.all()
        context['admin'] = self.request.user
        return context

