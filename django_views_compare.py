from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Account  # Assuming a basic Account model exists

# =====================================================================
# 0. Base View
# =====================================================================
class AccountLowLevelView(View):
    """
    Use cases: 
    absolute control over the HTTP request/response cycle.
     not dealing with standard database models, rendering templates, 
     a highly custom logic .
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
    Use Cases:
    a static HTML template, 
    injecting some basic context data. 
    Excellent for landing pages, "About Us" pages, or static dashboards.
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
    Use Cases:
    display a list of database records. 
    automatically handles querying the database, pagination, and passing the list to the template context.
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
    Use Cases:
    rendering a form to create a new database record.
    instantiating the form, validating the user's input, saving the 
    object to the database, and redirecting on success.
    """
    model = Account
    fields = ['account_number', 'account_type', 'balance']
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('account-list')

# =====================================================================
# 4. UpdateView
# =====================================================================
class AccountUpdateView(UpdateView):
    """
    Use Cases:
    update an existing database record via a form. 
    fetches the specific object using a URL parameter 
     populates the form with existing data, and handles updates.
    """
    model = Account
    fields = ['account_type', 'balance']
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('account-list')


# =====================================================================
# 5. DeleteView
# =====================================================================
class AccountDeleteView(DeleteView):
    """
    Use Cases:
    providing a confirmation page to delete an object from the database. 
    Upon a POST request to this view, the record is safely deleted.
    """
    model = Account
    template_name = 'accounts/account_confirm_delete.html'
    success_url = reverse_lazy('account-list')
