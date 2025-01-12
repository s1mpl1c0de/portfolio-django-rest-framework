from typing import Dict, Any

from django.core.exceptions import ValidationError


class ExperienceValidator:
    @staticmethod
    def validate_four_digit_year(value: int) -> None:
        if value < 1000 or value > 9999:
            raise ValidationError(f'{value} is not a valid year. It must be a 4-digit number.')

    @staticmethod
    def validate_data(data: Dict[str, Any]) -> Dict[str, Any]:
        is_still_in_role = data.get('is_still_in_role')
        started_year = data.get('started_year')
        started_month = data.get('started_month')
        ended_year = data.get('ended_year')
        ended_month = data.get('ended_month')
        errors = []

        if ended_year and started_year > ended_year:
            errors.append('Start year cannot be later than end year.')

        if started_year == ended_year and ended_month and started_month > ended_month:
            errors.append('Ended month cannot be earlier than started month.')

        if is_still_in_role and (ended_year or ended_month):
            errors.append('If still in role, ended year and ended month must not be provided.')

        if not is_still_in_role and (not ended_year or not ended_month):
            errors.append('If not still in role, both ended year and ended month must be provided.')

        if errors:
            raise ValidationError({'errors': errors})

        return data
