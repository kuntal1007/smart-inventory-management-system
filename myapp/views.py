from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Product
from .forms import ProductForm, SignUpForm
from django.db.models import Sum

def home(request):
    return render(request, 'myapp/home.html')

@login_required
def profile(request):
    return render(request, 'myapp/profile.html')

# Product List
@login_required
def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.filter(user=request.user)
    
    if query:
        products = products.filter(name__icontains= query)
    return render(request, 'myapp/product_list.html', {'products': products})

# Create Product
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'myapp/product_form.html', {'form': form})

# Update Product
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'myapp/product_form.html', {'form': form})

# Delete Product
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'myapp/product_confirm_delete.html', {'product': product})

# Sign Up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect('product_list')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

@login_required
def dashboard(request):
    products = Product.objects.filter(user = request.user)
    
    total_products = products.count()
    total_value = products.aggregate(Sum('price'))['price__sum'] or 0
    latest_products = products.order_by('-id')[:5]
    
    context = {
        'total_products': total_products,
        'total_value': total_value,
        'latest_products' : latest_products
    }
    
    return render(request, 'myapp/dashboard.html', context)