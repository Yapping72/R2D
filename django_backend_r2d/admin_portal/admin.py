from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from accounts.models import User
from authentication.models import FailedLoginAttempt
from django import forms
from django.http import HttpResponseForbidden
from accounts.models import User

"""
Superuser configuration
"""

class RootAdministrator(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'role')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


# Registers the default user model to superuser page
admin.site.register(User, RootAdministrator)
admin.site.unregister(Group)

# Form that is displayed to Staff Users
class StaffAdminUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'role']

class StaffAdminSite(admin.AdminSite):
    site_header = "R2D Administration"
    site_title = "R2D Administration"
    index_title = "Welcome R2D Administrator"

staff_admin_site = StaffAdminSite(name='staff_admin')

@admin.register(User, site=staff_admin_site)
class StaffAdministrator(BaseUserAdmin):
    form = StaffAdminUserChangeForm
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=False, is_superuser=False)
    
    def user_change_password(self, request, object_id, extra_context=None):
        return HttpResponseForbidden("Not allowed.")
    
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'is_active')}),
    )
    
    def has_change_permission(self, request, obj=None):
        if obj and obj == request.user:
            return False
        return super().has_change_permission(request, obj=obj)

    def has_add_permission(self, request):
        return False

    def has_module_permission(self, request):
        if (request.path.startswith('/manage/') and not request.path == '/manage/login/') and not request.user.is_superuser:
            return False
        return super().has_module_permission(request)

# Form for FailedLoginAttempt
class FailedLoginAttemptChangeForm(forms.ModelForm):
    class Meta:
        model = FailedLoginAttempt
        fields = ['user', 'failed_count']

# Register FailedLoginAttempt model for staff admin site
@admin.register(FailedLoginAttempt, site=staff_admin_site)
class FailedLoginAttemptAdmin(admin.ModelAdmin):
    form = FailedLoginAttemptChangeForm
    list_display = ('user', 'timestamp', 'failed_count')
    search_fields = ('user__username', 'user__email')
    actions = ['reset_failed_attempts']

    def reset_failed_attempts(self, request, queryset):
        for attempt in queryset:
            attempt.reset_failed_attempts()
        self.message_user(request, "Selected failed login attempts have been reset.")
    reset_failed_attempts.short_description = "Reset failed attempts"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    