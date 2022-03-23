from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile, User, UserActivity


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'fullname', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'email_verified',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'username', 'fullname', 'password1', 'password2')
            }
        ),
    )

    list_display = ('id', 'email', 'fullname', 'is_staff', 'last_login')
    list_display_links = ('id', 'email', 'fullname', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user',]
    list_display_links = [ 'user',]
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['login', 'logout']

admin.site.register(Profile, ProfileAdmin)
