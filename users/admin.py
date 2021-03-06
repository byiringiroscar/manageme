from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import Property_registration, Request_Property, Payment_report, ClientMessage

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
admin.site.register(Request_Property)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['phone_number', 'name', 'user_login', 'admin']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('phone_number', 'user_login', 'user_image', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'user_login', 'user_image', 'password', 'password_2')}
         ),
    )
    search_fields = ['phone_number']
    ordering = ['-id']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Property_registration)
admin.site.register(Payment_report)
admin.site.register(ClientMessage)

