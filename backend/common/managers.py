from django.db.models import Manager

from common.querysets import SoftDeleteQuerySet


class SoftDeleteManager(Manager):
    def __init__(self, only_deleted=False, with_deleted=False):
        self.only_deleted = only_deleted
        self.with_deleted = with_deleted
        super().__init__()

    def get_queryset(self):
        if self.only_deleted:
            return SoftDeleteQuerySet(self.model).only_deleted()

        if self.with_deleted:
            return SoftDeleteQuerySet(self.model)

        return SoftDeleteQuerySet(self.model).without_deleted()
