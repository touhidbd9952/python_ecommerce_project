from django.shortcuts import render, get_object_or_404, redirect

# Authentications
from django.contrib.auth.decorators import login_required

# Model
from App_Order.models import Cart, Order
from App_Shop.models import Product

# Messages
from django.contrib import messages


# Create your views here.

@login_required
def add_to_cart(request, pk):

    item = get_object_or_404(Product, pk=pk)   #get a record from "Product" by id
    
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)  #get a record from "Cart" by product id, current user and purchase=false
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)  #get all record from "Order" by current user and those record that prement not completed
    
    if order_qs.exists():    #if order table has record (current user)
        order = order_qs[0]  #string(comma seperated) need to convert to object
        
        if order.orderitems.filter(item=item).exists():  #if same product already exist in this order list
            order_item[0].quantity += 1  #increase cart (this) product quantity
            order_item[0].save()  #update cart
            messages.info(request, "This item quantity was updated.")
            return redirect("App_Shop:home")
        else:
            order.orderitems.add(order_item[0])  #add this product record in cart table
            messages.info(request, "This item was added to your cart.")
            return redirect("App_Shop:home")
    else:
        order = Order(user=request.user) #create a new record in Order table for this user
        order.save()
        order.orderitems.add(order_item[0])  #update Order table by cart product info
        messages.info(request, "This item was added to your cart.")
        return redirect("App_Shop:home")


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)  # get all info from cart table of this user that purchased status is false(not purchased)
    orders = Order.objects.filter(user=request.user, ordered=False)  # get all info from order table that order status is false(not premented)
    if carts.exists() and orders.exists(): #if record exist in both cart and order table
        order = orders[0] #convert to object
        return render(request, 'App_Order/cart.html', context={'carts':carts, 'order':order})
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect("App_Shop:home")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)  #get product info by id
    order_qs = Order.objects.filter(user=request.user, ordered=False) #get all info of this user from order table that order status is false(not premented)
    if order_qs.exists():  #if record exist in order table
        order = order_qs[0] #convert to object
        if order.orderitems.filter(item=item).exists():  #if product is exist in cart table
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0] #convert to object
            order.orderitems.remove(order_item) #remove this product from cart info of this order
            order_item.delete() #remove from cart
            messages.warning(request, "This item was removed form your cart")
            return redirect("App_Order:cart")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")

@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)  #get product info
    order_qs = Order.objects.filter(user=request.user, ordered=False) # get info from order table of this user that payment is not paid
    if order_qs.exists():   #if record exist in order table
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():  #if product info exist in cart
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False) #get info from cart table
            order_item = order_item[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect("App_Order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")


@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk) #get product info
    order_qs = Order.objects.filter(user=request.user, ordered=False) # get info from order table of this user that payment is not paid
    if order_qs.exists(): #if record exist in order table
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists(): #if product info exist in cart
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]  #get info from cart table
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect("App_Order:cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} item has been removed from your cart")
                return redirect("App_Order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")