from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Product, Category
from .forms import ProductForm, SignUpForm
from django.db.models import Sum
from django.db.models import Count


def home(request):
    return render(request, 'myapp/home.html')

@login_required
def profile(request):
    return render(request, 'myapp/profile.html')

# Product List
@login_required
def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    sort_by = request.GET.get('sort')
    
    products = Product.objects.filter(user=request.user)
    categories = Category.objects.all()
    
    if query:
        products = products.filter(name__icontains= query)
        
    if category_id:
        products = products.filter(category_id=category_id)
     
    if sort_by == "price_low":
        products = products.order_by("price")

    elif sort_by == "price_high":
        products = products.order_by("-price")

    elif sort_by == "newest":
        products = products.order_by("-id")

    elif sort_by == "oldest":
        products = products.order_by("id")

    elif sort_by == "stock_low":
        products = products.order_by("stock")

    elif sort_by == "stock_high":
        products = products.order_by("-stock") 
          
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'myapp/product_list.html', context)

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
    
    category_data = (
        products.values('category__name')
        .annotate(total=Count('id'))
    )
    
    labels=[]
    counts=[]
    
    for item in category_data:
        labels.append(item['category__name'] or "No Category")
        counts.append(item['total'])
    
    low_stock = products.filter(stock__gt = 0, stock__lte =5).count()
    out_of_stock = products.filter(stock=0).count()
    total_categories = products.values('category').distinct().count()
    
    context = {
        'total_products': total_products,
        'total_value': total_value,
        'latest_products' : latest_products,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'total_categoreis': total_categories,
        'labels': labels,
        'counts': counts,
    }
    
    return render(request, 'myapp/dashboard.html', context)