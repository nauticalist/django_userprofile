from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import CreateUserForm, UpdateUserForm
from .models import User


class UserAdmin(BaseUserAdmin):
    add_form = CreateUserForm
    form = UpdateUserForm
    model = User
    list_display = ['email', 'first_name', 'last_name',
                    'date_of_birth']
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name',
                           'last_name', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'bio', 'avatar', 'city',
                                      'state', 'country', 'favorite_animal',
                                      'hobbies')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active',
                                    'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name',
                       'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'bio', 'avatar', 'city',
                                      'state', 'country', 'favorite_animal',
                                      'hobbies')}),
    )
    ordering = ['-date_joined']


admin.site.register(User, UserAdmin)
