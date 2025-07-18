from django.shortcuts import render, redirect

from item.models import Category, Item

from .forms import SignupForm

def index(request):
    items = Item.objects.filter(status='active', admin_approved=True)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def featured(request):
    return render(request, 'core/featured.html')

def order_protection(request):
    return render(request, 'core/order_protection.html')

def become_supplier(request):
    return render(request, 'core/become_supplier.html')

def help_center(request):
    return render(request, 'core/help_center.html')

def buyer_central(request):
    return render(request, 'core/buyer_central.html')

def faq(request):
    return render(request, 'core/faq.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })