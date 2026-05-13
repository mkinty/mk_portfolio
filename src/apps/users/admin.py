from django.contrib import admin

from apps.users.models import User

# Register your models here.


# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "is_active")
    list_filter = ("is_active",)
    search_fields = ("first_name", "last_name", "email")
