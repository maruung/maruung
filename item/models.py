from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    CATEGORY_TYPES = [
        # Electronics & Technology
        ('electronics', 'Electronics & Technology'),
        ('phones_tablets', 'Phones & Tablets'),
        ('computers_laptops', 'Computers & Laptops'),
        ('cameras_photo', 'Cameras & Photography'),
        ('audio_headphones', 'Audio & Headphones'),
        ('gaming_consoles', 'Gaming & Consoles'),
        ('smart_home', 'Smart Home & IoT'),
        ('wearable_tech', 'Wearable Technology'),
        
        # Vehicles & Transportation
        ('cars', 'Cars & Automobiles'),
        ('motorcycles', 'Motorcycles & Scooters'),
        ('bicycles', 'Bicycles & E-bikes'),
        ('trucks_commercial', 'Trucks & Commercial Vehicles'),
        ('auto_parts', 'Auto Parts & Accessories'),
        ('boats_marine', 'Boats & Marine'),
        
        # Real Estate & Property
        ('houses_sale', 'Houses for Sale'),
        ('apartments_rent', 'Apartments for Rent'),
        ('commercial_property', 'Commercial Property'),
        ('land_plots', 'Land & Plots'),
        ('vacation_rentals', 'Vacation Rentals'),
        
        # Fashion & Beauty
        ('mens_clothing', "Men's Clothing"),
        ('womens_clothing', "Women's Clothing"),
        ('shoes_footwear', 'Shoes & Footwear'),
        ('bags_accessories', 'Bags & Accessories'),
        ('jewelry_watches', 'Jewelry & Watches'),
        ('beauty_cosmetics', 'Beauty & Cosmetics'),
        
        # Home & Garden
        ('furniture', 'Furniture'),
        ('home_decor', 'Home Decor'),
        ('kitchen_dining', 'Kitchen & Dining'),
        ('garden_outdoor', 'Garden & Outdoor'),
        ('tools_hardware', 'Tools & Hardware'),
        ('appliances', 'Home Appliances'),
        
        # Sports & Recreation
        ('sports_equipment', 'Sports Equipment'),
        ('fitness_gym', 'Fitness & Gym'),
        ('outdoor_camping', 'Outdoor & Camping'),
        ('bicycles_sports', 'Sports Bicycles'),
        ('water_sports', 'Water Sports'),
        
        # Services
        ('professional_services', 'Professional Services'),
        ('home_services', 'Home Services'),
        ('tutoring_education', 'Tutoring & Education'),
        ('health_wellness', 'Health & Wellness'),
        ('event_services', 'Event Services'),
        ('business_services', 'Business Services'),
        ('legal_services', 'Legal Services'),
        ('financial_services', 'Financial Services'),
        
        # Jobs & Employment
        ('full_time_jobs', 'Full-time Jobs'),
        ('part_time_jobs', 'Part-time Jobs'),
        ('freelance_gigs', 'Freelance & Gigs'),
        ('internships', 'Internships'),
        ('remote_work', 'Remote Work'),
        
        # Baby & Kids
        ('baby_items', 'Baby Items'),
        ('kids_clothing', 'Kids Clothing'),
        ('toys_games', 'Toys & Games'),
        ('baby_gear', 'Baby Gear'),
        ('educational_toys', 'Educational Toys'),
        
        # Books & Media
        ('books', 'Books'),
        ('movies_music', 'Movies & Music'),
        ('magazines', 'Magazines'),
        ('educational_materials', 'Educational Materials'),
        
        # Pets & Animals
        ('pets_sale', 'Pets for Sale'),
        ('pet_supplies', 'Pet Supplies'),
        ('pet_services', 'Pet Services'),
        ('livestock', 'Livestock'),
        
        # Food & Agriculture
        ('fresh_produce', 'Fresh Produce'),
        ('packaged_foods', 'Packaged Foods'),
        ('agricultural_products', 'Agricultural Products'),
        ('farming_equipment', 'Farming Equipment'),
        
        # Art & Collectibles
        ('artwork', 'Artwork'),
        ('antiques', 'Antiques'),
        ('collectibles', 'Collectibles'),
        ('crafts_handmade', 'Crafts & Handmade'),
        
        # Business & Industrial
        ('office_supplies', 'Office Supplies'),
        ('industrial_equipment', 'Industrial Equipment'),
        ('business_equipment', 'Business Equipment'),
        ('wholesale_bulk', 'Wholesale & Bulk'),
        
        # Other
        ('other', 'Other'),
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