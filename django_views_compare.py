from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Account  # Assuming a basic Account model exists

# =====================================================================
# 0. Base View
# =====================================================================
class AccountLowLevelView(View):
    """
    WHEN TO CHOOSE: 
    When you need absolute control over the HTTP request/response cycle.
    Use this if you are not dealing with standard database models, rendering 
    templates, or if you're building highly custom logic (like a webhook receiver).
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("Custom low-level GET response")

    def post(self, request, *args, **kwargs):
        return HttpResponse("Custom low-level POST response")


# =====================================================================
# 1. TemplateView
# =====================================================================
class AccountDashboardView(TemplateView):
    """
    WHEN TO CHOOSE:
    When you just need to render a static HTML template, optionally 
    injecting some basic context data. Excellent for landing pages, 
    "About Us" pages, or static dashboards.
    """
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Account Dashboard"
        return context


# =====================================================================
# 2. ListView
# =====================================================================
class AccountListView(ListView):
    """
    WHEN TO CHOOSE:
    When your primary goal is to display a list of database records. 
    It automatically handles querying the database, pagination, and 
    passing the list to the template context.
    """
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'  # Overrides default 'object_list'
    paginate_by = 10


# =====================================================================
# 3. CreateView
# =====================================================================
class AccountCreateView(CreateView):
    """
    WHEN TO CHOOSE:
    When rendering a form to create a new database record. It handles 
    instantiating the form, validating the user's input, saving the 
    object to the database, and redirecting on success.
    """
    model = Account
    fields = ['account_number', 'account_type', 'balance']
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('account-list')

