from typing import Dict, Any

from rest_framework import serializers

from apps.jobs.helpers import ExperienceHelper
from apps.jobs.models import Experience
from apps.jobs.validators import ExperienceValidator


class ExperienceWritableSerializer(serializers.ModelSerializer):
    ended_month = serializers.IntegerField(allow_null=True)
    ended_year = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Experience
        fields = [
            'job_title', 'description', 'company_name', 'started_month',
            'ended_month', 'started_year', 'ended_year', 'is_still_in_role'
        ]

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return ExperienceValidator.validate_data(data)


class ExperienceReadableSerializer(serializers.ModelSerializer):
    working_period = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = ['uuid', 'job_title', 'description', 'company_name', 'working_period']

    @staticmethod
    def get_working_period(experience: Experience) -> str:
        return ExperienceHelper.get_working_period(experience)
