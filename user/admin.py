from django.contrib import admin
from .models import UserProfile,Wallet
# Register your models here.


admin.site.register(UserProfile)
admin.site.site_header = "QFS Admin"
admin.site.site_title = "QFS Admin Portal"
admin.site.index_title = "Welcome to the QFS Admin Portal"



admin.site.register(Wallet)