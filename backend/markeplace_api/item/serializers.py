from rest_framework import serializers
from .models import Category, Item, ItemImage, Brand, DriveType, EngineType, ItemPrice, Reservation
from .fields import Base64ImageField

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

# class CarModelSerializer(serializers.ModelSerializer):
#     brand = BrandSerializer(read_only=True)

#     class Meta:
#         model = CarModel
#         fields = ['name', 'brand']

class DriveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveType
        fields = ['id', 'name']

class EngineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineType
        fields = ['id', 'name']

class ItemImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = ItemImage
        fields = ['image', 'image_url']

    def get_image_url(self, obj):
        return obj.image_url()


class ItemPriceSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), write_only=True, required=False)

    class Meta:
        model = ItemPrice
        fields = ['item', 'title', 'price']

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    drive = serializers.PrimaryKeyRelatedField(queryset=DriveType.objects.all())
    engine_type = serializers.PrimaryKeyRelatedField(queryset=EngineType.objects.all())
    prices = ItemPriceSerializer(many=True)
    images = ItemImageSerializer(many=True, required=False, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'category', 'brand', 'car_model', 'title', 'description', 'prices', 'deposit', 'distance_limit', 'price_per_addicional_distance', 'car_power', 'acceleration', 
            'automatic_gearbox', 'drive', 'engine_size', 'engine_type', 'max_speed', 'year',
            'created_by', 'created_by_email',  'created_at', 'updated_at', 'images', 'location', 'delivery_to_customer', 'offert_type'
        ]
    
    def create(self, validated_data):
        prices_data = validated_data.pop('prices', [])  
        images_data = validated_data.pop('images', [])
        item = Item.objects.create(**validated_data)  

        for price_data in prices_data:
            ItemPrice.objects.create(item=item, **price_data)

        for image_data in images_data:
            ItemImage.objects.create(item=item, **image_data)

        return item



class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id', 'item_id', 'item_title', 'start_date', 'end_date', 'number_of_days', 'details_from_customer', 'customer_name', 'customer_surname', 'customer_phonenumber', 'customer_city', 'customer_mail', 'company_mail', 'company_name', 'company_visible_mail', 'company_phonenumber', 'company_website', 'company_city'
        ]