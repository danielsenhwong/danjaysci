from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest

from _compact import JsonResponse
from django import forms

from django.views import generic

import django_excel as excel

from .models import Vendor, WebAccount, SupplyCategory, Item, Quote, ItemPrice, Order, LineItem, ItemRequest

class UploadFileForm(forms.Form):
    file = forms.FileField()

# Create your views here.
def index(request):
    items = Item.objects.order_by('name')
    context = {
        'items': items
    }
    return render(request, 'supplies/index.html', context)

def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        
        # define a function to pull IDs for associated models
        
        
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models = [
                
                ]
            )
            return HttpResponse("OK", status=200)
        else:
            return HttpResponseBadRequest()

def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            # Convert Excel sheet from get_sheet() to a csv and download as download.csv
            return excel.make_response(filehandle.get_sheet(), "csv", file_name="download")
    else:
        form = UploadFileForm()
    return render_to_reponse("upload_form.html", {"form": form}, context_instance=RequestContext(request))

class OrderListView(generic.ListView):
    template_name = 'order/index.html'
    context_object_name = 'recent_order_list'

    def get_queryset(self):
        return Order.objects.order_by('date_ordered')[:5]

class QuoteListView(generic.ListView):
    template_name = 'quote/index.html'
    context_object_name = 'quote_list'

    def get_queryset(self):
        return Quote.objects.order_by('-valid_until', 'vendor')

class RequestListView(generic.ListView):
    template_name = 'itemrequest/index.html'
    context_object_name = 'request_list'

    def get_queryset(self):
        return ItemRequest.objects.filter(denied=False, order_line_item=None, ordered_by=None).order_by('date_requested')

class SupplyListView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'current_supply_list'

    def get_queryset(self):
        return Item.objects.order_by('name')

class SupplyCategoryListView(generic.ListView):
    template_name = 'supplycategory/index.html'
    context_object_name = 'supplycategory_list'

    def get_queryset(self):
        return SupplyCategory.objects.order_by('name')

class VendorListView(generic.ListView):
    template_name = 'vendor/index.html'
    context_object_name = 'vendor_list'
    
    def get_queryset(self):
        return Vendor.objects.order_by('name')

class WebAccountListView(generic.ListView):
    template_name = 'webaccount/index.html'
    context_object_name = 'webaccount_list'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order/detail.html'

class SupplyDetailView(generic.DetailView):
    model = Item
    template_name = 'detail.html'
