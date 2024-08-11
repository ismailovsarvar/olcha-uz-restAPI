from rest_framework import status, generics

from olchauz import models, serializers

"""PRODUCT GENERIC API VIEW"""


class ProductCreateApiView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'message': 'Product Successfully Created'}
        response.status_code = status.HTTP_201_CREATED
        return response


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer
    lookup_field = 'slug'

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
