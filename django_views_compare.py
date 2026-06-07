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

