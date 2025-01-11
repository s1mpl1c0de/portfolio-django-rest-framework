from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from common.constants import WRITABLE_ACTIONS, PARTIAL_UPDATE


class ReadWritableSerializerMixin(GenericViewSet):
    writable_serializer = None
    readable_serializer = None
    create_serializer = None
    list_serializer = None
    retrieve_serializer = None
    update_serializer = None
    partial_update_serializer = None

    def get_serializer_class(self):
        action = self.action
        if self.is_writable_action(action):
            return self.get_writable_serializer(action)
        return self.get_readable_serializer(action)

    @staticmethod
    def is_writable_action(action):
        return action in WRITABLE_ACTIONS

    def get_writable_serializer(self, action):
        if action == PARTIAL_UPDATE:
            return (
                    self.partial_update_serializer or
                    self.update_serializer or
                    super().get_serializer_class()
            )

        return (
                self.writable_serializer or
                getattr(self, f'{action}_serializer', None) or
                super().get_serializer_class()
        )

    def get_readable_serializer(self, action):
        return (
                self.readable_serializer or
                getattr(self, f'{action}_serializer', None) or
                super().get_serializer_class()
        )


class CreateModelMixin(GenericViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created_at=timezone.now(), created_user=self.request.user)

    @staticmethod
    def get_success_headers(data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class UpdateModelMixin(GenericViewSet):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response()

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now(), updated_user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(GenericViewSet):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete(user=self.request.user)
