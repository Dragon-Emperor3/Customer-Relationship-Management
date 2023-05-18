from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from django.http import HttpResponse
from .models import *
from .forms import *

from .filters import FilterOrder

from .decorators import un_authenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group


# Create your views here.

# Creater and Login User Section
@un_authenticated_user
def registerPage(request):

# we have remove the it here and wrote the same code in decorators.py
#  if request.user.is_authenticated:
#     return redirect('home')
# else:
    form= CreateUserForm()    
    if(request.method== 'POST'):
        form= CreateUserForm(request.POST)
        if(form.is_valid()):
            user= form.save()
            username= form.cleaned_data.get('username')

            # We have moved all this logic to signals.py
            # group= Group.objects.get(name= 'customer')
            # user.groups.add(group)
            # Customer.objects.create(user= user, name= user.username)
            messages.success(request, 'Account has created for '+ username)
            return redirect('login')
        else:  
             messages.error(request, 'Invalid Fields!!!')

    context={'form':form}
    return render(request, 'accounts/register.html', context)


@un_authenticated_user
def loginPage(request):

# we have remove the it here and wrote the same code in decorators.py
#  if request.user.is_authenticated:
#     return redirect('home')
# else:
    if(request.method=="POST"):
        username= request.POST.get('username')
        password= request.POST.get('password')

        user= authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is Incorrect')


    context={}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


#Website pages
@login_required(login_url='login')
@admin_only
def home(request):

    orders= Order.objects.all()
    lastest_orders= Order.objects.order_by('-date_created')
    customers= Customer.objects.all()

    total_customers= customers.count()
    total_orders= orders.count()

    delivered= orders.filter(status='Delivered').count()
    pending= orders.filter(status='Pending').count()


    context= {'latest_orders':lastest_orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def user(request):
    orders= request.user.customer.order_set.all()
    latest_orders= request.user.customer.order_set.order_by('-date_created')#This will show new orders at top

    total_orders= latest_orders.count()
    delivered= latest_orders.filter(status='Delivered').count()
    pending= latest_orders.filter(status='Pending').count()

    myFilter= FilterOrder(request.GET, queryset=latest_orders)
    latest_orders= myFilter.qs

    context={'orders':latest_orders, 'total_orders':total_orders,'myFilter':myFilter,
                'delivered':delivered, 'pending':pending
             }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):

    customer= request.user.customer
    form= CustomerForm(instance=customer)
    if(request.method=="POST"):
        form= CustomerForm(request.POST, request.FILES, instance=customer)
        if(form.is_valid):
            form.save()
            return redirect('account')

    context={'form':form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products= Product.objects.all()
    
    return render(request, 'accounts/products.html',{'products':products})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, primary_key):
    customer= Customer.objects.get(id=primary_key)

    orders= customer.order_set.all()
    orders_count= orders.count()    

    myFilter= FilterOrder(request.GET, queryset=orders)
    orders= myFilter.qs

    context= {'customer': customer,'orders':orders ,'orders_count': orders_count, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)


#Order Related
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request, pk):
    
    #OrderFormSet= inlineformset_factory(Customer, Order, fields=['product', 'status'], extra=5)
    customer= Customer.objects.get(id=pk)
    form= OrderForm(initial={'customer':customer})
    #formset= OrderFormSet(queryset= Order.objects.none(), instance=customer)
    if(request.method== 'POST'):
        # print('Printing Post',request.POST)
        form= OrderForm(request.POST)
        #formset= OrderFormSet(request.POST, instance=customer)
        if(form.is_valid()):
            form.save()
        return redirect('/')

    context= {'form':form}
    return render(request, 'accounts/order_form.html', context)



@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, primary_key):
    
    order= Order.objects.get(id=primary_key)
    form= OrderForm(instance=order)
    
    if(request.method== 'POST'):
        form= OrderForm(request.POST, instance=order)
        if(form.is_valid()):
            form.save()
        return redirect('/')

    context= {'form':form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk):

    order= Order.objects.get(id=pk)


    if(request.method== "POST"):
        order.delete()
        return redirect('/')
    
    context={'order': order}
    return render(request, 'accounts/delete_order.html', context)


# Products Related
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createProduct(request):
    form= ProductForm()
    if(request.method=='POST'):
        form= ProductForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('products')

    context={'form':form}
    return render(request, 'accounts/productForm/createForm.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form= ProductForm(instance=product)
    if(request.method=='POST'):
        form= ProductForm(request.POST, instance= product)
        if(form.is_valid()):
            form.save()
            return redirect('products')

    context={'form':form}
    return render(request, 'accounts/productForm/createForm.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteProduct(request, pk):

    product= Product.objects.get(id=pk)


    if(request.method== "POST"):
        product.delete()
        return redirect('products')
    
    context={'product': product}
    return render(request, 'accounts/productForm/delete_product.html', context)


# Tags Related
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def tagHome(request):
    tag= Tag.objects.all()
    context={'tag':tag}
    return render(request, 'accounts/tagForm/taghome.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createTag(request):
    form= TagForm()
    if(request.method=='POST'):
        form= TagForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('tag')

    context={'form':form}
    return render(request, 'accounts/tagForm/createTag.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateTag(request, pk):
    tag= Tag.objects.get(id=pk)

    form= TagForm(instance=tag)
    if(request.method=='POST'):
        form= TagForm(request.POST, instance=tag)
        if(form.is_valid()):
            form.save()
            return redirect('tag')

    context={'form':form}
    return render(request, 'accounts/tagForm/createTag.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteTag(request, pk):

    tag= Tag.objects.get(id=pk)


    if(request.method== "POST"):
        tag.delete()
        return redirect('tag')
    
    context={'tag': tag}
    return render(request, 'accounts/tagForm/deleteTag.html', context)