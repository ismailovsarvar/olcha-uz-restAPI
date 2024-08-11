from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from olchauz import models, serializers

"""CATEGORY API VIEW"""


class CategoryListApiView(APIView):

    def get(self, request):
        categories = models.Category.objects.all()
        serializer = serializers.CategoryModelSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.CategoryModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Category Successfully Created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailApiView(APIView):

    def get(self, request, slug):
        category = models.Category.objects.get(slug=slug)
        serializer = serializers.CategoryModelSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        category = models.Category.objects.get(slug=slug)
        serializer = serializers.CategoryModelSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Category Successfully Updated', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        category = models.Category.objects.get(slug=slug)
        category.delete()
        return Response('Category Successfully Deleted', status=status.HTTP_200_OK)


"""CATEGORY GENERICS VIEW"""


class CategoryListCreateApiView(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryModelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Category Successfully Created'}, status=status.HTTP_201_CREATED)


class CategoryDetailGenericApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryModelSerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Category Successfully Updated'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Category Successfully Deleted'}, status=status.HTTP_200_OK)
