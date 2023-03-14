from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import ChatGroup, Message
from chat.serializers import ChatGroupSerializer, ChatGroupAddUserSerializer, MessageSerializer, LikeSerializer
from users.models import Profile
from users.serializers import ProfileSerializer


class ChatGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ChatGroup.objects.all()

    def list(self, request):
        serializer = ChatGroupSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = ChatGroupSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        serializer = ChatGroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={'message': 'Chat Group created'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def add_profile(self, request, pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = ChatGroupAddUserSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={'message': 'User added to Chat Group'}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def list_profiles(self, request, pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        profile_serializer = ProfileSerializer( instance.profiles, many=True)
        return Response(profile_serializer.data)

    @action(methods=['delete'], detail=True)
    def remove_profile(self, request, pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        profile = get_object_or_404(instance.profiles, pk=request.data.get("profile"))
        instance.profiles.remove(profile)
        return Response(status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()

    # todo list messages by group
    def list(self, request):
        serializer = MessageSerializer(self.queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = MessageSerializer(instance, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        serializer = MessageSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        if instance.profile == request.user.profile:
            instance.delete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def like(self, request, pk):
        data = request.data

        message = get_object_or_404(Message.objects.all(), id=pk)
        # if message.profile == request.user.profile:
        #     return Response({'message': 'You can\'t like your own message'}, status.HTTP_400_BAD_REQUEST)

        updated_data = data.copy()
        updated_data.update({"message": message.id})

        serializer = LikeSerializer(data=updated_data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
