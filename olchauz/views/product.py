from django.http import Http404
from rest_framework import status, generics, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from olchauz import models, serializers
from olchauz.permissions import CustomPermission

"""PRODUCT GENERIC API VIEW"""


class ProductCreateApiView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        group_slug = self.kwargs['group_slug']
        # queryset = models.Product.objects.filter(group__category__slug=category_slug, group__slug=group_slug)

        # Optimization
        queryset = models.Product.objects.filter(group__category__slug=category_slug,
                                                 group__slug=group_slug).select_related('group', 'group__category')
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'message': 'Product Successfully Created'}
        response.status_code = status.HTTP_201_CREATED
        return response


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):

    # Optimization
    queryset = models.Product.objects.select_related('group', 'group__category').all()

    # queryset = models.Product.objects.all()
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


"""Permissions"""


class ProductViewSet(viewsets.ModelViewSet):
    # Optimization
    queryset = models.Product.objects.select_related('group', 'group__category').prefetch_related('is_liked')

    # queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer
    permission_classes = [CustomPermission]
