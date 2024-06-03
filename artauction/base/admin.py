from django.contrib import admin

# Register your models here.
from .models import User, Category, Item, Bid, Collection

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(Collection)
