from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorites, name='favorites'),
    path('settings/', views.settings, name='settings'),
    path('toggle-favorite/<int:item_id>/', views.toggle_favorite, name='toggle_favorite'),
]