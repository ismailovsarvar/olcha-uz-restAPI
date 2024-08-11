from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework.views import APIView

from olchauz import models, serializers

"""GROUP GENERICS VIEW"""


class GroupCreateApiView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupModelSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return models.Group.objects.filter(category__slug=slug)

# class GroupListApiView(APIView):
#
#     def get(self, request):
#         groups = models.Group.objects.all()
#         serializer = serializers.GroupModelSerializer(groups, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)


class GroupDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupModelSerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response('Group Successfully Updated', status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Group Successfully Deleted', status=status.HTTP_200_OK)
