from rest_framework import serializers

from olchauz.models import Category


class CategoryModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Category
        fields = '__all__'
