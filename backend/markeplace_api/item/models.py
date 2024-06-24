from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

# class CarModel(models.Model):
#     name = models.CharField(max_length=255)
#     brand = models.ForeignKey(Brand, related_name='car_models', on_delete=models.CASCADE, default=1) 

#     class Meta:
#         verbose_name_plural = 'Car Models'

#     def __str__(self):
#         return f'{self.brand.name} {self.name}'

    
class DriveType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Drive Types'

    def __str__(self):
        return self.name
    
class EngineType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Engine Types'

    def __str__(self):
        return self.name

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=False)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE, default=1)
    brand = models.ForeignKey(Brand, related_name='items', on_delete=models.CASCADE, default=1)
    # car_model = models.ForeignKey(CarModel, related_name='items', on_delete=models.CASCADE, default=1)
    car_model = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    car_power = models.IntegerField(default=0)
    acceleration = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)
    automatic_gearbox = models.BooleanField(default=True)
    drive = models.ForeignKey(DriveType, related_name='items', on_delete=models.CASCADE, default=1)
    engine_size = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)
    engine_type = models.ForeignKey(EngineType, related_name='items', on_delete=models.CASCADE, default=1)
    max_speed = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE)
    created_by_email = models.CharField(max_length=255, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255)
    delivery_to_customer = models.BooleanField(default=True)
    deposit =  models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    distance_limit = models.IntegerField(default=0)
    price_per_addicional_distance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    offert_type = models.CharField(max_length=255, default=1)


    class Meta:
        verbose_name_plural = 'Items'

    def __str__(self):
        status = 'active' if self.is_active else 'XXX'
        return f'[{status}] - {self.id} - {self.title}'
    
class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')

    def __str__(self):
        return f'Image for {self.item.title}'
    
    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'
    
class ItemPrice(models.Model):
    item = models.ForeignKey(Item, related_name='prices', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'Price for {self.item.title}'
    
    def formatted_price(self):
        return self.price
    
class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.IntegerField(default=1)
    item_title = models.CharField(max_length=255, default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_days = models.IntegerField()
    created_by = models.CharField(max_length=255, default=1)
    details_from_customer = models.TextField()
    customer_name = models.CharField(max_length=255, default=1)
    customer_surname = models.CharField(max_length=255, default=1)
    customer_phonenumber = models.CharField(max_length=255, default=1)
    customer_mail = models.CharField(max_length=255, default=1)
    customer_city = models.CharField(max_length=255, default=1)
    
    company_mail = models.CharField(max_length=255, default=1)
    company_name = models.CharField(max_length=255, default=1)
    company_visible_mail = models.CharField(max_length=255, default=1)
    company_phonenumber = models.CharField(max_length=255, default=1)
    company_website = models.CharField(max_length=255, default=1)
    company_city = models.CharField(max_length=255, default=1)


    def __str__(self):
        return f'{self.id} - {self.item_title}'
