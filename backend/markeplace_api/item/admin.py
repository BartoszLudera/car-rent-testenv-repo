from django.contrib import admin
from .models import Category, Item, ItemImage, Brand, DriveType, EngineType, ItemPrice, Reservation

class ItemPriceInline(admin.TabularInline):
    model = ItemPrice
    extra = 1

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemPriceInline, ItemImageInline]

class ItemPriceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category)
admin.site.register(Brand)
# admin.site.register(CarModel)
admin.site.register(ItemPrice, ItemPriceAdmin) 
admin.site.register(DriveType)
admin.site.register(EngineType)
admin.site.register(Item, ItemAdmin)
admin.site.register(Reservation)
