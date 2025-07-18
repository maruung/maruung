from django.core.management.base import BaseCommand
from item.models import Category

class Command(BaseCommand):
    help = 'Create initial categories for Matrix Marketplace'

    def handle(self, *args, **options):
        categories = [
            # Electronics & Technology
            {'name': 'Mobile Phones & Tablets', 'slug': 'phones-tablets', 'category_type': 'phones_tablets', 'icon': 'fas fa-mobile-alt'},
            {'name': 'Computers & Laptops', 'slug': 'computers-laptops', 'category_type': 'computers_laptops', 'icon': 'fas fa-laptop'},
            {'name': 'Cameras & Photography', 'slug': 'cameras-photo', 'category_type': 'cameras_photo', 'icon': 'fas fa-camera'},
            {'name': 'Audio & Headphones', 'slug': 'audio-headphones', 'category_type': 'audio_headphones', 'icon': 'fas fa-headphones'},
            {'name': 'Gaming & Consoles', 'slug': 'gaming-consoles', 'category_type': 'gaming_consoles', 'icon': 'fas fa-gamepad'},
            {'name': 'Smart Home & IoT', 'slug': 'smart-home', 'category_type': 'smart_home', 'icon': 'fas fa-home'},
            
            # Vehicles & Transportation
            {'name': 'Cars & Automobiles', 'slug': 'cars', 'category_type': 'cars', 'icon': 'fas fa-car'},
            {'name': 'Motorcycles & Scooters', 'slug': 'motorcycles', 'category_type': 'motorcycles', 'icon': 'fas fa-motorcycle'},
            {'name': 'Bicycles & E-bikes', 'slug': 'bicycles', 'category_type': 'bicycles', 'icon': 'fas fa-bicycle'},
            {'name': 'Auto Parts & Accessories', 'slug': 'auto-parts', 'category_type': 'auto_parts', 'icon': 'fas fa-cog'},
            
            # Fashion & Beauty
            {'name': "Men's Clothing", 'slug': 'mens-clothing', 'category_type': 'mens_clothing', 'icon': 'fas fa-tshirt'},
            {'name': "Women's Clothing", 'slug': 'womens-clothing', 'category_type': 'womens_clothing', 'icon': 'fas fa-female'},
            {'name': 'Shoes & Footwear', 'slug': 'shoes-footwear', 'category_type': 'shoes_footwear', 'icon': 'fas fa-shoe-prints'},
            {'name': 'Bags & Accessories', 'slug': 'bags-accessories', 'category_type': 'bags_accessories', 'icon': 'fas fa-shopping-bag'},
            {'name': 'Jewelry & Watches', 'slug': 'jewelry-watches', 'category_type': 'jewelry_watches', 'icon': 'fas fa-gem'},
            
            # Home & Garden
            {'name': 'Furniture', 'slug': 'furniture', 'category_type': 'furniture', 'icon': 'fas fa-couch'},
            {'name': 'Home Decor', 'slug': 'home-decor', 'category_type': 'home_decor', 'icon': 'fas fa-paint-brush'},
            {'name': 'Kitchen & Dining', 'slug': 'kitchen-dining', 'category_type': 'kitchen_dining', 'icon': 'fas fa-utensils'},
            {'name': 'Garden & Outdoor', 'slug': 'garden-outdoor', 'category_type': 'garden_outdoor', 'icon': 'fas fa-seedling'},
            {'name': 'Home Appliances', 'slug': 'appliances', 'category_type': 'appliances', 'icon': 'fas fa-blender'},
            
            # Services
            {'name': 'Professional Services', 'slug': 'professional-services', 'category_type': 'professional_services', 'icon': 'fas fa-briefcase'},
            {'name': 'Home Services', 'slug': 'home-services', 'category_type': 'home_services', 'icon': 'fas fa-tools'},
            {'name': 'Tutoring & Education', 'slug': 'tutoring-education', 'category_type': 'tutoring_education', 'icon': 'fas fa-graduation-cap'},
            {'name': 'Health & Wellness', 'slug': 'health-wellness', 'category_type': 'health_wellness', 'icon': 'fas fa-heartbeat'},
            
            # Jobs & Employment
            {'name': 'Full-time Jobs', 'slug': 'full-time-jobs', 'category_type': 'full_time_jobs', 'icon': 'fas fa-user-tie'},
            {'name': 'Part-time Jobs', 'slug': 'part-time-jobs', 'category_type': 'part_time_jobs', 'icon': 'fas fa-clock'},
            {'name': 'Freelance & Gigs', 'slug': 'freelance-gigs', 'category_type': 'freelance_gigs', 'icon': 'fas fa-laptop-code'},
            
            # Real Estate
            {'name': 'Houses for Sale', 'slug': 'houses-sale', 'category_type': 'houses_sale', 'icon': 'fas fa-home'},
            {'name': 'Apartments for Rent', 'slug': 'apartments-rent', 'category_type': 'apartments_rent', 'icon': 'fas fa-building'},
            {'name': 'Commercial Property', 'slug': 'commercial-property', 'category_type': 'commercial_property', 'icon': 'fas fa-store'},
            
            # Sports & Recreation
            {'name': 'Sports Equipment', 'slug': 'sports-equipment', 'category_type': 'sports_equipment', 'icon': 'fas fa-football-ball'},
            {'name': 'Fitness & Gym', 'slug': 'fitness-gym', 'category_type': 'fitness_gym', 'icon': 'fas fa-dumbbell'},
            
            # Baby & Kids
            {'name': 'Baby Items', 'slug': 'baby-items', 'category_type': 'baby_items', 'icon': 'fas fa-baby'},
            {'name': 'Kids Clothing', 'slug': 'kids-clothing', 'category_type': 'kids_clothing', 'icon': 'fas fa-child'},
            {'name': 'Toys & Games', 'slug': 'toys-games', 'category_type': 'toys_games', 'icon': 'fas fa-puzzle-piece'},
            
            # Pets & Animals
            {'name': 'Pets for Sale', 'slug': 'pets-sale', 'category_type': 'pets_sale', 'icon': 'fas fa-paw'},
            {'name': 'Pet Supplies', 'slug': 'pet-supplies', 'category_type': 'pet_supplies', 'icon': 'fas fa-bone'},
            
            # Books & Media
            {'name': 'Books', 'slug': 'books', 'category_type': 'books', 'icon': 'fas fa-book'},
            {'name': 'Movies & Music', 'slug': 'movies-music', 'category_type': 'movies_music', 'icon': 'fas fa-music'},
            
            # Other
            {'name': 'Other', 'slug': 'other', 'category_type': 'other', 'icon': 'fas fa-ellipsis-h'},
        ]

        created_count = 0
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories')
        )