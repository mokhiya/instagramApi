from django.contrib import admin

from users.models import CustomUser, VerificationModel

admin.site.register(CustomUser)
admin.site.register(VerificationModel)