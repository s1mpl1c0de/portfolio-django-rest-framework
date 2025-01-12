from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from common.utils import generate_uuid


class UserProfile(AbstractUser):
    uuid = models.CharField(max_length=100, editable=False, unique=True)

    class Meta:
        db_table = 'accounts_user_profile'
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = generate_uuid(self.__class__.__name__)

        super().save(*args, **kwargs)


User = get_user_model()
