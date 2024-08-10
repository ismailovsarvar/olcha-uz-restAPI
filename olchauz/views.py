from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from olchauz import models, serializers


"""CATEGORY VIEW"""


class CategoryListApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        categories = models.Category.objects.all()
        serializer = serializers.CategoryModelSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.CategoryModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Product Successfully Created', status=status.HTTP_201_CREATED)
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
            return Response('Product Successfully Updated', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        category = models.Category.objects.get(slug=slug)
        category.delete()
        return Response('Product Successfully Deleted', status=status.HTTP_200_OK)


"""PRODUCT VIEW"""

