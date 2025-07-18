from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('featured/', views.featured, name='featured'),
    path('order-protection/', views.order_protection, name='order_protection'),
    path('become-supplier/', views.become_supplier, name='become_supplier'),
    path('help-center/', views.help_center, name='help_center'),
    path('buyer-central/', views.buyer_central, name='buyer_central'),
    path('faq/', views.faq, name='faq'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
]
