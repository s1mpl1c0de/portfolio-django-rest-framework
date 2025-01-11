from django.db.models import QuerySet
from django.utils import timezone


class SoftDeleteQuerySet(QuerySet):
    def only_deleted(self):
        return self.filter(deleted_at__isnull=False, deleted_user__isnull=False)

    def without_deleted(self):
        return self.filter(deleted_at__isnull=True, deleted_user__isnull=True)

    def delete(self, hard=False, user=None):
        if hard:
            return super().delete()

        return super().update(deleted_at=timezone.now(), deleted_user=user)

    def restore(self):
        return super().update(deleted_at=None, deleted_user=None)
