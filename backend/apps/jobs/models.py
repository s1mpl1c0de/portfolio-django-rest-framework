from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.accounts.models import User
from apps.jobs.validators import ExperienceValidator
from common.models import Model


class Experience(Model):
    job_title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    company_name = models.CharField(max_length=255)
    started_month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    started_year = models.PositiveSmallIntegerField(validators=[ExperienceValidator.validate_four_digit_year])
    ended_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)])
    ended_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[ExperienceValidator.validate_four_digit_year]
    )
    is_still_in_role = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')

    class Meta(Model.Meta):
        pass
