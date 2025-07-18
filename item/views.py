from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import NewItemForm, EditItemForm, ItemFilterForm
from .models import Category, Item, ItemView, ItemFavorite
from accounts.models import Report

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def items(request):
    form = ItemFilterForm(request.GET)
    items = Item.objects.filter(status='active', admin_approved=True)
    categories = Category.objects.filter(is_active=True).order_by('name')
    
    # Apply filters
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        condition = form.cleaned_data.get('condition')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        location = form.cleaned_data.get('location')
        delivery_available = form.cleaned_data.get('delivery_available')
        pickup_available = form.cleaned_data.get('pickup_available')
        is_negotiable = form.cleaned_data.get('is_negotiable')
        sort_by = form.cleaned_data.get('sort_by', 'newest')
        
        if query:
            items = items.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )
        
        if category:
            items = items.filter(category=category)
        
        if condition:
            items = items.filter(condition__in=condition)
        
        if min_price is not None:
            items = items.filter(price__gte=min_price)
        
        if max_price is not None:
            items = items.filter(price__lte=max_price)
        
        if location:
            items = items.filter(location__icontains=location)
        
        if delivery_available:
            items = items.filter(delivery_available=True)
        
        if pickup_available:
            items = items.filter(pickup_available=True)
        
        if is_negotiable:
            items = items.filter(is_negotiable=True)
        
        # Sorting
        if sort_by == 'oldest':
            items = items.order_by('created_at')
        elif sort_by == 'price_low':
            items = items.order_by('price')
        elif sort_by == 'price_high':
            items = items.order_by('-price')
        elif sort_by == 'most_viewed':
            items = items.order_by('-views')
        elif sort_by == 'most_favorited':
            items = items.order_by('-favorites')
        else:  # newest
            items = items.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'items': page_obj,
        'categories': categories,
        'form': form,
        'total_items': items.count(),
    }
    
    return render(request, 'item/items.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk, status='active', admin_approved=True)
    related_items = Item.objects.filter(
        category=item.category, 
        status='active', 
        admin_approved=True
    ).exclude(pk=pk)[:3]
    
    # Track view
    ip_address = get_client_ip(request)
    view, created = ItemView.objects.get_or_create(
        item=item,
        user=request.user if request.user.is_authenticated else None,
        ip_address=ip_address
    )
    
    if created:
        Item.objects.filter(pk=pk).update(views=F('views') + 1)
    
    # Check if user has favorited this item
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = ItemFavorite.objects.filter(item=item, user=request.user).exists()
    
    context = {
        'item': item,
        'related_items': related_items,
        'is_favorited': is_favorited,
        'item_images': item.get_all_images(),
    }
    
    return render(request, 'item/detail.html', context)

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(request, 'Your item has been listed successfully!')
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    categories = Category.objects.filter(is_active=True).order_by('name')
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
        'categories': categories,
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your item has been updated successfully!')
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
        'item': item,
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    messages.success(request, 'Your item has been deleted successfully!')
    return redirect('dashboard:index')

@login_required
@require_POST
def toggle_favorite(request, pk):
    item = get_object_or_404(Item, pk=pk)
    favorite, created = ItemFavorite.objects.get_or_create(item=item, user=request.user)
    
    if not created:
        favorite.delete()
        Item.objects.filter(pk=pk).update(favorites=F('favorites') - 1)
        favorited = False
    else:
        Item.objects.filter(pk=pk).update(favorites=F('favorites') + 1)
        favorited = True
    
    return JsonResponse({
        'favorited': favorited,
        'favorites_count': item.favorites
    })

@login_required
@require_POST
def report_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    report_type = request.POST.get('report_type')
    description = request.POST.get('description', '')
    
    if report_type:
        Report.objects.create(
            reporter=request.user,
            reported_item=item,
            reported_user=item.created_by,
            report_type=report_type,
            description=description
        )
        
        # Mark item as reported
        item.is_reported = True
        item.save()
        
        messages.success(request, 'Thank you for your report. We will review it shortly.')
    
    return redirect('item:detail', pk=pk)