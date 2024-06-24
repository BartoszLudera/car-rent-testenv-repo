from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'visible_name', 'contact_email', 'contact_phonenumber', 'website', 'logo', 'city', 'nip', 'regulamin', 'marketing']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            visible_name=validated_data.get('visible_name', ''),
            contact_email=validated_data.get('contact_email', ''),
            contact_phonenumber=validated_data.get('contact_phonenumber', ''),
            website=validated_data.get('website', ''),
            city=validated_data.get('city', ''),
            nip=validated_data.get('nip', ''),
            regulamin=validated_data.get('regulamin', False),
            marketing=validated_data.get('marketing', False),
        )
        if 'logo' in validated_data:
            user.logo = validated_data['logo']
        user.set_password(validated_data['password'])
        user.save()
        return user
