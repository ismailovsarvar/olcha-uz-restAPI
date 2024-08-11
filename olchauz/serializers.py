from rest_framework import serializers

from olchauz.models import Category, Group, Product, Attribute, Key, Value


class CategoryModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Category
        fields = '__all__'


class GroupModelSerializer(serializers.ModelSerializer):
    # category = CategoryModelSerializer(read_only=True)
    category_title = serializers.CharField(source='category.title')
    category_slug = serializers.SlugField(source='category.slug')
    image = serializers.SerializerMethodField(method_name='foo')

    def foo(self, obj):
        image_url = obj.image.url
        request = self.context.get('request')
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Group
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class KeyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'


class ValueModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = '__all__'


class AttributeModelSerializer(serializers.ModelSerializer):
    key = KeyModelSerializer(read_only=True)
    value = ValueModelSerializer(read_only=True)
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = Attribute
        fields = '__all__'
