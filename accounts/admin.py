from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserProfile, AdminAction, Report, UserReview

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = (
        'phone_number', 'profile_picture', 'bio', 'location', 'country',
        'account_type', 'is_verified', 'verification_status', 'rating',
        'is_suspended', 'suspension_reason'
    )

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_verification_status', 'get_is_suspended', 'get_profile_picture')
    list_filter = BaseUserAdmin.list_filter + ('profile__is_verified', 'profile__is_suspended', 'profile__account_type')
    actions = ['suspend_users', 'unsuspend_users', 'verify_users']
    
    def get_verification_status(self, obj):
        if hasattr(obj, 'profile'):
            status = obj.profile.verification_status
            colors = {'verified': 'green', 'pending': 'orange', 'rejected': 'red'}
            return format_html(
                '<span style="color: {};">{}</span>',
                colors.get(status, 'black'),
                status.title()
            )
        return 'No Profile'
    get_verification_status.short_description = 'Verification'
    
    def get_is_suspended(self, obj):
        return obj.profile.is_suspended if hasattr(obj, 'profile') else False
    get_is_suspended.boolean = True
    get_is_suspended.short_description = 'Suspended'
    
    def get_profile_picture(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return format_html('<img src="{}" width="30" height="30" style="border-radius: 50%;" />', obj.profile.profile_picture.url)
        return 'No Image'
    get_profile_picture.short_description = 'Picture'
    
    def suspend_users(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.is_suspended = True
                user.profile.suspension_reason = f"Suspended by admin {request.user.username}"
                user.profile.save()
                
                AdminAction.objects.create(
                    admin=request.user,
                    target_user=user,
                    action_type='suspend_user',
                    reason=f"Bulk suspension by {request.user.username}"
                )
        self.message_user(request, f"{queryset.count()} users have been suspended.")
    suspend_users.short_description = "Suspend selected users"
    
    def unsuspend_users(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.is_suspended = False
                user.profile.suspension_reason = ""
                user.profile.save()
                
                AdminAction.objects.create(
                    admin=request.user,
                    target_user=user,
                    action_type='unsuspend_user',
                    reason=f"Bulk unsuspension by {request.user.username}"
                )
        self.message_user(request, f"{queryset.count()} users have been unsuspended.")
    unsuspend_users.short_description = "Unsuspend selected users"
    
    def verify_users(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.is_verified = True
                user.profile.verification_status = 'verified'
                user.profile.save()
                
                AdminAction.objects.create(
                    admin=request.user,
                    target_user=user,
                    action_type='verify_user',
                    reason=f"Bulk verification by {request.user.username}"
                )
        self.message_user(request, f"{queryset.count()} users have been verified.")
    verify_users.short_description = "Verify selected users"

@admin.register(AdminAction)
class AdminActionAdmin(admin.ModelAdmin):
    list_display = ('admin', 'action_type', 'target_user', 'target_item', 'timestamp')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('admin__username', 'target_user__username', 'reason')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'report_type', 'reported_user', 'reported_item', 'status', 'created_at')
    list_filter = ('report_type', 'status', 'created_at')
    search_fields = ('reporter__username', 'reported_user__username', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_resolved', 'mark_as_dismissed', 'mark_as_investigating']
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved', resolved_by=request.user)
        self.message_user(request, f"{queryset.count()} reports marked as resolved.")
    mark_as_resolved.short_description = "Mark selected reports as resolved"
    
    def mark_as_dismissed(self, request, queryset):
        queryset.update(status='dismissed', resolved_by=request.user)
        self.message_user(request, f"{queryset.count()} reports marked as dismissed.")
    mark_as_dismissed.short_description = "Mark selected reports as dismissed"
    
    def mark_as_investigating(self, request, queryset):
        queryset.update(status='investigating', resolved_by=request.user)
        self.message_user(request, f"{queryset.count()} reports marked as investigating.")
    mark_as_investigating.short_description = "Mark selected reports as investigating"

@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewed_user', 'rating', 'item', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer__username', 'reviewed_user__username', 'comment')
    readonly_fields = ('created_at',)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Customize admin site
admin.site.site_header = "Matrix Marketplace Admin"
admin.site.site_title = "Matrix Admin"
admin.site.index_title = "Welcome to Matrix Marketplace Administration"