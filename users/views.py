from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from circle.permissions import NonSuperuserReadOnlyPermission
from users.models import Profile
from users.serializers import UserWriteSerializer, UserUpdateSerializer, ProfileSerializer, UserReadSerializer


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = (NonSuperuserReadOnlyPermission,)
    action_permissions = {
        IsAuthenticated: ['list', 'retrieve'],
        IsAdminUser: ['create', 'partial_update', 'destroy']
    }

    def list(self, request):
        serializer = UserReadSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = UserReadSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserWriteSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = UserUpdateSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def list(self, request):
        serializer = ProfileSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = ProfileSerializer(instance)
        return Response(serializer.data)
