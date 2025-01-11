from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.mixins import CreateModelMixin, UpdateModelMixin
from apps.accounts.models import User
from apps.accounts.serializers import (
    UserReadableSerializer, UserCreateSerializer, UserUpdateSerializer
)
from common.mixins import ReadWritableSerializerMixin


class UserViewSet(CreateModelMixin, UpdateModelMixin, ReadWritableSerializerMixin, ModelViewSet):
    queryset = User.objects.all()
    create_serializer = UserCreateSerializer
    update_serializer = UserUpdateSerializer
    readable_serializer = UserReadableSerializer
    lookup_field = 'uuid'

    @action(detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
