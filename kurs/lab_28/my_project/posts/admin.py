from django.contrib import admin

from .models import Posts, CustomUser

admin.site.register(Posts)
admin.site.register(CustomUser)
