from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField

class UserProfile(models.Model):
    ACCOUNT_TYPES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
    ]
    
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = PhoneNumberField(blank=True, null=True)
    profile_picture = CloudinaryField('profile_pics', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    country = CountryField(blank=True, null=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='individual')
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    is_suspended = models.BooleanField(default=False)
    suspension_reason = models.TextField(blank=True)
    
    # Business fields
    business_name = models.CharField(max_length=100, blank=True)
    business_registration = models.CharField(max_length=50, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=False)
    
    # Theme preference
    theme_preference = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()
    
    @property
    def display_name(self):
        return self.full_name if self.full_name else self.user.username

class AdminAction(models.Model):
    ACTION_TYPES = [
        ('suspend_user', 'Suspend User'),
        ('unsuspend_user', 'Unsuspend User'),
        ('remove_listing', 'Remove Listing'),
        ('verify_user', 'Verify User'),
        ('reject_verification', 'Reject Verification'),
        ('warning', 'Warning'),
        ('ban_user', 'Ban User'),
        ('feature_listing', 'Feature Listing'),
        ('unfeature_listing', 'Unfeature Listing'),
    ]
    
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_actions')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_actions', null=True, blank=True)
    target_item = models.ForeignKey('item.Item', on_delete=models.CASCADE, null=True, blank=True)
    action_type = models.CharField(max_length=30, choices=ACTION_TYPES)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.admin.username} - {self.action_type} - {self.timestamp}"

class Report(models.Model):
    REPORT_TYPES = [
        ('inappropriate_content', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('fraud', 'Fraud'),
        ('fake_listing', 'Fake Listing'),
        ('harassment', 'Harassment'),
        ('counterfeit', 'Counterfeit Products'),
        ('prohibited_items', 'Prohibited Items'),
        ('misleading_info', 'Misleading Information'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received', null=True, blank=True)
    reported_item = models.ForeignKey('item.Item', on_delete=models.CASCADE, null=True, blank=True)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_reports')
    
    def __str__(self):
        return f"Report by {self.reporter.username} - {self.report_type}"

class UserReview(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    item = models.ForeignKey('item.Item', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['reviewer', 'reviewed_user', 'item']
    
    def __str__(self):
        return f"{self.reviewer.username} -> {self.reviewed_user.username} ({self.rating}★)"