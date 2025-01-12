from django.utils import timezone

from apps.jobs.models import Experience
from apps.jobs.serializers import ExperienceWritableSerializer, ExperienceReadableSerializer
from common.permissions import IsAdminUserOrReadOnly
from common.viewsets import ModelViewSet


class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    writable_serializer = ExperienceWritableSerializer
    readable_serializer = ExperienceReadableSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_at=timezone.now(), created_user=self.request.user, user=self.request.user)
