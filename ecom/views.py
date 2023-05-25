from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import F,Aggregate,Sum
#local imports 

from base.utils import Manage_base_view,SuperuserRedirectPermission
from .models import *
from .forms import Product_add_form


class Product_page(Manage_base_view):

    def homepage(self,request,*args,**kwargs):
        '''
        shows the list of products in the home page
        '''
        listings = Product.is_active.all()
        if request.user.is_authenticated:
            count = Cart.is_active.filter(created_by = request.user).aggregate(total_quantity = Sum('quantity')).get('total_quantity')
        return render(request,'homepage.html',locals())
    
    def show_cart(self,request,*args,**kwargs):
        '''
        view for showing the cart contents 
        '''
        if request.user.is_authenticated:
            listing = Cart.is_active.filter(created_by= request.user)
            return render(request,'cart.html',locals())
        else:
            return redirect('login')
  
    def update_quantity(self,request,*args,**kwargs):
        slug_id,operation = self.request.GET.get('data').split(" ")
        try:
            if slug_id and operation:
                cart = Cart.is_active.get(product_name__slug_field = slug_id)
            
                if operation == "remove":
                    if cart.quantity > 1:
                        cart.quantity -= 1
                        cart.price -= cart.product_name.price
                elif operation == 'add':
                    cart.quantity += 1
                    cart.price += cart.product_name.price
                cart.save()
        except Exception as e:  
            print(e)
        return JsonResponse({'data':cart.price})
    
    def update_cart(self,request,*args,**kwargs):
        data = self.request.GET.get('data')
        product = Product.is_active.get(id=data)
        if self.request.user.is_authenticated:
            cart_item, created = Cart.is_active.get_or_create(
                created_by=self.request.user,
                product_name=product,
            )

            if created:
                cart_item.quantity = 1
                cart_item.price = product.price

            else:
                cart_item.quantity = F('quantity') + 1
                cart_item.price += product.price

            cart_item.save()
            return JsonResponse({'data':1})
        else:
            return redirect('login')
        
    def remove_cart(self,request,*args,**kwargs):
        slug_id = kwargs.get('slug')
        try:
            cart = Cart.is_active.get(product_name__slug_field = slug_id).delete()
        except Exception as e:
            print(str(e))
            return redirect('cart')
        return redirect('cart')

class Product_crud(SuperuserRedirectPermission,Manage_base_view):
    '''
    only superuser can access the product crud
    '''

    def list_products(self,request,*args,**kwargs):
        listing = Product.is_active.all()
        return render(request,'product_list.html',locals())
        
    def add_product(self,request,*args,**kwargs):
        form = Product_add_form
        if request.method  == 'POST':
            form = Product_add_form(request.POST,request.FILES)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.created_by = self.request.user
                form_data.save()
                return redirect('list_products')
        return render(request,'add_form.html',locals())
    

    def edit_product(self,request,*args,**kwargs):
        slug = kwargs.get('slug')
        try:
            product = Product.is_active.get(slug_field = slug)
        except:
            return redirect('list_products')
        
        if request.method == 'POST':
            form = Product_add_form(request.POST,request.FILES,instance = product)
            if form.is_valid():
                user = form.save(commit=False)
                user.created_by = self.request.user
                user.save()
                return redirect("list_products")
        form = Product_add_form(instance = product)
        return render(request,'add_form.html',locals())
    
    def delete_product(self,request,*args,**kwargs):
        print(f'args{args},keargs{kwargs}')
        if request.method == 'POST':
            data = request.POST.get('deletevalue',None)
            if data:
                product = Product.is_active.get(slug_field = data).delete()
                return redirect("list_products")
        return redirect('list_products')