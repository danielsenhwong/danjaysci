from django.shortcuts import render

from django.http import HttpResponse

from django.views.generic.detail import DetailView

from .models import Institution, Department, Program, Group, Funding

# Create your views here.
def index(request):
    return HttpResponse("Hello!")


class InstitutionDetailView(DetailView):
    model = Institution

    def get_context_data(self, **kwargs):
        context = super(InstitutionDetailView, self).get_context_data(**kwargs)
        return context
