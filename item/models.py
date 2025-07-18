from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    CATEGORY_TYPES = [
        ('electronics', 'Electronics & Appliances'),
        ('fashion_beauty', 'Fashion & Beauty'),
        ('home_furniture', 'Home & Furniture'),
        ('vehicles_auto', 'Vehicles & Auto Parts'),
        ('property_real_estate', 'Property & Real Estate'),
        ('jobs_services', 'Jobs & Services'),
        ('agriculture_food', 'Agriculture & Food'),
        ('health_wellness', 'Health & Wellness'),
        ('kids_baby', 'Kids & Baby'),
        ('education_training', 'Education & Training'),
        ('events_entertainment', 'Events & Entertainment'),
        ('others', 'Others'),
    ]
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPES, default='other')
    icon = models.CharField(max_length=50, default='fas fa-tag')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Brand New'),
        ('like_new', 'Like New'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
        ('removed', 'Removed by Admin'),
        ('expired', 'Expired'),
    ]
    
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Images using Cloudinary
    image = CloudinaryField('item_images', blank=True, null=True)
    image_2 = CloudinaryField('item_images', blank=True, null=True)
    image_3 = CloudinaryField('item_images', blank=True, null=True)
    image_4 = CloudinaryField('item_images', blank=True, null=True)
    image_5 = CloudinaryField('item_images', blank=True, null=True)
    
    # Location and delivery
    location = models.CharField(max_length=255, blank=True)
    delivery_available = models.BooleanField(default=False)
    pickup_available = models.BooleanField(default=True)
    
    # Engagement metrics
    views = models.PositiveIntegerField(default=0)
    favorites = models.PositiveIntegerField(default=0)
    
    # Flags and moderation
    is_featured = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    is_negotiable = models.BooleanField(default=True)
    is_reported = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=True)
    removal_reason = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['status', 'admin_approved']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_sold(self):
        return self.status == 'sold'
    
    @property
    def is_active(self):
        return self.status == 'active' and self.admin_approved
    
    def get_all_images(self):
        images = []
        for i in range(1, 6):
            img = getattr(self, f'image{"" if i == 1 else f"_{i}"}', None)
            if img:
                images.append(img.url)
        return images

class ItemView(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['item', 'user', 'ip_address']

class ItemFavorite(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_items')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['item', 'user']