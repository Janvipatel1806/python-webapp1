from django.contrib import admin
from .models import User,SUser,Additem,Wishlist,Cart
# Register your models here.
admin.site.register(User)
admin.site.register(SUser)
admin.site.register(Additem)
admin.site.register(Wishlist)
admin.site.register(Cart)
