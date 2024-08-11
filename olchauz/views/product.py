from django.http import Http404
from rest_framework import status, generics
from rest_framework.exceptions import NotFound

from olchauz import models, serializers

"""PRODUCT GENERIC API VIEW"""


class ProductCreateApiView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        group_slug = self.kwargs['group_slug']
        queryset = models.Product.objects.filter(group__category__slug=category_slug, group__slug=group_slug)
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'message': 'Product Successfully Created'}
        response.status_code = status.HTTP_201_CREATED
        return response


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer
    lookup_field = 'slug'

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound({'message': 'Product not found with the provided slug.'})

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'message': 'Product Successfully Updated'}
        response.status_code = status.HTTP_200_OK
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'message': 'Product Successfully Deleted'}
        response.status_code = status.HTTP_200_OK
        return response


"""PRODUCT ATTRIBUTE API VIEW"""


class ProductAttributeCreateApiView(generics.ListCreateAPIView):
    queryset = models.Attribute.objects.all()
    serializer_class = serializers.AttributeModelSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'message': 'Product Attribute Successfully Created'}
        response.status_code = status.HTTP_201_CREATED
        return response


class ProductAttributeDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Attribute.objects.all()
    serializer_class = serializers.AttributeModelSerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'message': 'Product Attribute Successfully Updated'}
        response.status_code = status.HTTP_200_OK
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'message': 'Product Attribute Successfully Deleted'}
        response.status_code = status.HTTP_200_OK
        return response
