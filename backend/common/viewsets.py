from rest_framework import viewsets

from common.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ReadWritableSerializerMixin
)


class ModelViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ReadWritableSerializerMixin,
    viewsets.ModelViewSet
):
    lookup_field = 'uuid'
