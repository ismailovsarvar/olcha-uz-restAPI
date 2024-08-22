from django.db.models import Avg
from django_auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from django.utils.translation import gettext_lazy as _
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
    product_count = serializers.SerializerMethodField()

    def get_product_count(self, instance):
        return instance.products.count()

    def foo(self, obj):
        image_url = obj.image.url
        request = self.context.get('request')
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Group
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='group.category.title')
    group_name = serializers.CharField(source='group.title')
    is_liked = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    comment_info = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attrs = instance.attributes.all().values('key__name', 'value__name')
        # product_attributes = [
        #     {
        #         attribute['key__name']: attribute['value__name'],
        #     }
        #     for attribute in attrs
        # ]
        combined_attrs = {attr['key__name']: attr['value__name'] for attr in attrs}
        print(combined_attrs)
        # return combined_attrs

    def get_comment_info(self, obj):
        # comments = [
        #     {
        #         'message': comment.message,
        #         'rating': comment.rating,
        #         'username': comment.user.username,
        #
        #     }
        #     for comment in obj.comments.all()
        # ]
        # return comments

        return obj.comments.all().values('message', 'rating', 'user__username')

    def get_all_images(self, instance):
        request = self.context.get('request', None)
        images = instance.images.all().order_by('-is_primary', '-id')
        all_images = []
        for image in images:
            all_images.append(request.build_absolute_uri(image.image.url))
        return all_images

    def get_avg_rating(self, product):
        avg_rating = product.comments.all().aggregate(avg=Avg('rating'))
        return avg_rating.get('avg')

    def get_images(self, obj):
        # image = Image.objects.filter(is_primary=True, product=obj).first()
        image = obj.images.filter(is_primary=True).first()
        if image:
            image_url = image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url)

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user in obj.is_liked.all():
                return True
            return False

    class Meta:
        model = Product
        fields = '__all__'


"""AUTH SERIALIZER"""


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=255, required=True)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, required=True, write_only=True)
    password2 = serializers.CharField(max_length=255, required=True, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, username):
        # username = self.validated_data['username']
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exist!"
            }
            raise ValidationError(detail=detail)
        return username

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({"message": "Both password must match"})

        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({"message": "Email already taken!"})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')

        # Create the User
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create a token for the user
        Token.objects.create(user=user)
        return user


"""END AUTH SERIALIZER"""


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
