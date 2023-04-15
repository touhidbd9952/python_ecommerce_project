from django.shortcuts import render

# Import django builtin views to see all product listview and single product detailview
from django.views.generic import ListView, DetailView

# Add your Models
from App_Shop.models import Product

# Add Mixin for sequrity. mixins used for class based view
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'
    # return object_list = select * from Product

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'App_Shop/product_detail.html'
    #return object = select * from Product where id=id
