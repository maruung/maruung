from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Item, ItemView, ItemFavorite
from accounts.models import AdminAction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'parent', 'is_active', 'items_count', 'created_at')
    list_filter = ('category_type', 'is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)

    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items Count'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'created_by', 'price', 'condition', 'status',
        'admin_approved', 'is_featured', 'views', 'favorites', 'created_at', 'get_image'
    )
    list_filter = (
        'status', 'condition', 'admin_approved', 'is_featured',
        'is_reported', 'category', 'created_at'
    )
    search_fields = ('name', 'description', 'created_by__username', 'location')
    readonly_fields = ('views', 'favorites', 'created_at', 'updated_at')
    list_editable = ('admin_approved', 'is_featured', 'status')
    date_hierarchy = 'created_at'
    actions = ['approve_items', 'remove_items', 'feature_items', 'unfeature_items']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'price', 'condition')
        }),
        ('Images', {
            'fields': ('image', 'image_2', 'image_3', 'image_4', 'image_5')
        }),
        ('Location & Delivery', {
            'fields': ('location', 'delivery_available', 'pickup_available')
        }),
        ('Status & Flags', {
            'fields': (
                'status', 'admin_approved', 'is_featured',
                'is_urgent', 'is_negotiable', 'is_reported'
            )
        }),
        ('Moderation', {
            'fields': ('removal_reason',)
        }),
        ('Metrics', {
            'fields': ('views', 'favorites', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )

    def get_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return 'No Image'
    get_image.short_description = 'Image'

    def approve_items(self, request, queryset):
        queryset.update(admin_approved=True, status='active')
        for item in queryset:
            AdminAction.objects.create(
                admin=request.user,
                target_item=item,
                target_user=item.created_by,
                action_type='approve_listing',
                reason=f"Bulk approval by {request.user.username}"
            )
        self.message_user(request, f"{queryset.count()} items have been approved.")
    approve_items.short_description = "Approve selected items"

    def remove_items(self, request, queryset):
        queryset.update(admin_approved=False, status='removed')
        for item in queryset:
            AdminAction.objects.create(
                admin=request.user,
                target_item=item,
                target_user=item.created_by,
                action_type='remove_listing',
                reason=f"Bulk removal by {request.user.username}"
            )
        self.message_user(request, f"{queryset.count()} items have been removed.")
    remove_items.short_description = "Remove selected items"

    def feature_items(self, request, queryset):
        queryset.update(is_featured=True)
        for item in queryset:
            AdminAction.objects.create(
                admin=request.user,
                target_item=item,
                target_user=item.created_by,
                action_type='feature_listing',
                reason=f"Bulk featuring by {request.user.username}"
            )
        self.message_user(request, f"{queryset.count()} items have been featured.")
    feature_items.short_description = "Feature selected items"

    def unfeature_items(self, request, queryset):
        queryset.update(is_featured=False)
        for item in queryset:
            AdminAction.objects.create(
                admin=request.user,
                target_item=item,
                target_user=item.created_by,
                action_type='unfeature_listing',
                reason=f"Bulk unfeaturing by {request.user.username}"
            )
        self.message_user(request, f"{queryset.count()} items have been unfeatured.")
    unfeature_items.short_description = "Unfeature selected items"


@admin.register(ItemView)
class ItemViewAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'ip_address', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('item__name', 'user__username', 'ip_address')
    readonly_fields = ('timestamp',)


@admin.register(ItemFavorite)
class ItemFavoriteAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('item__name', 'user__username')
    readonly_fields = ('created_at',)
