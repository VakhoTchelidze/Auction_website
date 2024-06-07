from django.contrib import admin

# Register your models here.
from .models import User, Category, Item, Bid, Collection, Comment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(Collection)
admin.site.register(Comment)