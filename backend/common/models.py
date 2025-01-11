from django.conf import settings
from django.db import models
from django.utils import timezone

from common.managers import SoftDeleteManager
from common.utils import generate_uuid


class Timestamp(models.Model):
    uuid = models.CharField(
        max_length=100,
        editable=False,
        unique=True,
    )
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_%(class)s',
        editable=False,
    )
    updated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='updated_%(class)s',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = generate_uuid(self.__class__.__name__)

        super().save(*args, **kwargs)


class SoftDelete(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='deleted_%(class)s',
        null=True,
        blank=True,
    )

    objects = SoftDeleteManager()
    objects_deleted = SoftDeleteManager(only_deleted=True)
    objects_with_deleted = SoftDeleteManager(with_deleted=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, hard=False, user=None):
        if hard:
            return super().delete(using, keep_parents)

        self.deleted_at = timezone.now()
        self.deleted_user = user
        self.save()

    def restore(self):
        self.deleted_at = None
        self.deleted_user = None
        self.save()


class Model(Timestamp, SoftDelete, models.Model):
    class Meta:
        abstract = True
        ordering = ['-created_at']
