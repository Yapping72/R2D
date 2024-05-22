from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from accounts.models import User
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

    # Override the queryset to exclude staff and superusers
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=False, is_superuser=False)
    
    # Remove the password change option
    def user_change_password(self, request, object_id, extra_context=None):
        return HttpResponseForbidden("Not allowed.")
    
    # Override fieldsets to exclude permissions and password
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'is_active')}),
    )
    
    # Disallow staff from adding their own permissions
    def has_change_permission(self, request, obj=None):
        if obj and obj == request.user:
            return False
        return super().has_change_permission(request, obj=obj)

    # Hide the "Add" permission for User model
    def has_add_permission(self, request):
        return False

    # Prevents access to the admin page 
    def has_module_permission(self, request):
        if (request.path.startswith('/admin/') and not request.path == '/admin/login/') and not request.user.is_superuser:
            return False
        return super().has_module_permission(request)
