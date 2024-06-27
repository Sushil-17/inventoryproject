from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction

# Create your views here.
@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    product_count = products.count()
    workers_count = User.objects.all().count()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user

            # Update product quantity  after getting order from the staff.
            product_id = form.cleaned_data['product'].id
            quantity_ordered = form.cleaned_data['order_quantity']
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product_id)
                if product.quantity >= quantity_ordered:
                    product.quantity -= quantity_ordered
                    product.save()
                else:
                    messages.error(request, f'Insufficient quantity available for {product.name}.')
                    return redirect('dashboard-index')
            
            instance.save()
            messages.success(request, 'Order placed successfully.') #line from 
            return redirect('dashboard-index')
           #end of new code 
    else:
        form = OrderForm()
    context = {
        'orders' : orders,
        'form' : form,
        'products' : products,
        'product_count':product_count,
        'workers_count':workers_count,
        'orders_count':orders_count,
    }
    return render(request, 'dashboard/index.html',context)

@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'workers' : workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/staff.html',context)

def staff_detail(request,pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers' : workers,

    }
    return render(request, 'dashboard/staff_detail.html',context)

@login_required
def product(request):
    items = Product.objects.all()
    # items = Product.objects.raw('SELECT * FROM dashboard_product')
    product_count = items.count()
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'Request for {product_name} has been made.')
            
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'items' : items,
        'form' : form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count' : product_count,
    }
    return render(request, 'dashboard/product.html',context)

def product_delete(request,pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request,'dashboard/product_delete.html')

def product_update(request,pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance= item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/product_update.html',context)

@login_required
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'orders' : orders,
        'workers_count' : workers_count,
        'orders_count' : orders_count,
        'product_count' : product_count,
    }
    
    return render(request, 'dashboard/order.html',context)


#logic code for approve and reject button but not working.

# @login_required
# def approve_order(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     # Implement your logic to approve the order here
#     # Example:
#     order.status = 'Approved'
#     order.save()
#     messages.success(request, f'Order {order.pk} has been approved.')
#     return redirect('dashboard-order')

# @login_required
# def reject_order(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     # Implement your logic to reject the order here
#     # Example:
#     order.status = 'Rejected'
#     order.save()
#     messages.success(request, f'Order {order.pk} has been rejected.')
#     return redirect('dashboard-order')
