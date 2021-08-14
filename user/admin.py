from django.contrib import admin

# Register your models here.
from user.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'phone', 'city', 'country'#, 'image_tag']
    ] # i commented out the image_tag so it cant display


admin.site.register(UserProfile, UserProfileAdmin)
