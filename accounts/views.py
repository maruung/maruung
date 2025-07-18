from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import UserProfile
from .forms import UserProfileForm
from item.models import Item, ItemFavorite

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def favorites(request):
    favorite_items = ItemFavorite.objects.filter(user=request.user).select_related('item')
    
    context = {
        'favorite_items': favorite_items,
    }
    return render(request, 'accounts/favorites.html', context)

@login_required
@require_POST
def toggle_favorite(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    favorite, created = ItemFavorite.objects.get_or_create(item=item, user=request.user)
    
    if not created:
        favorite.delete()
        favorited = False
        item.favorites = max(0, item.favorites - 1)
    else:
        favorited = True
        item.favorites += 1
    
    item.save()
    
    return JsonResponse({
        'favorited': favorited,
        'favorites_count': item.favorites
    })

@login_required
def settings(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle theme preference
        theme = request.POST.get('theme', 'light')
        profile.theme_preference = theme
        profile.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('accounts:settings')
    
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/settings.html', context)