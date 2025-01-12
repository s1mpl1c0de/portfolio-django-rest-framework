import calendar
from typing import Optional

from django.utils import timezone

from apps.jobs.models import Experience


class ExperienceHelper:
    @staticmethod
    def get_working_period(experience: Experience) -> str:
        total_months_worked = ExperienceHelper.calculate_total_months_worked(experience)
        years_worked, months_worked = ExperienceHelper.calculate_years_months_worked(total_months_worked)
        started_month_abbr = ExperienceHelper.get_month_abbr_from_month_number(experience.started_month)
        ended = (
            'Present'
            if experience.is_still_in_role
            else f'{ExperienceHelper.get_month_abbr_from_month_number(experience.ended_month)} {experience.ended_year}'
        )
        working_period = f'{started_month_abbr} {experience.started_year} - {ended}'
        working_period += ExperienceHelper.append_duration(years_worked, months_worked)
        return working_period

    @staticmethod
    def calculate_total_months_worked(experience: Experience) -> int:
        current_datetime = timezone.now()
        started_year = experience.started_year
        started_month = experience.started_month

        total_months_worked = (
                ((current_datetime.year - started_year) * 12) +
                (current_datetime.month - started_month + 1)
        )
        if not experience.is_still_in_role:
            total_months_worked = (
                    ((experience.ended_year - started_year) * 12) +
                    (experience.ended_month - started_month + 1)
            )

        return total_months_worked

    @staticmethod
    def calculate_years_months_worked(total_months_worked: int) -> tuple:
        years_worked = total_months_worked // 12
        months_worked = total_months_worked % 12
        return years_worked, months_worked

    @staticmethod
    def get_month_abbr_from_month_number(number: Optional[int]) -> Optional[str]:
        return calendar.month_abbr[number] if number else None

    @staticmethod
    def append_duration(years_worked: int, months_worked: int) -> str:
        year_label = 'year' if years_worked == 1 else 'years'
        month_label = 'month' if months_worked == 1 else 'months'
        duration = ''

        if years_worked > 0 and months_worked > 0:
            duration = f' ({years_worked} {year_label} {months_worked} {month_label})'
        elif years_worked > 0:
            duration = f' ({years_worked} {year_label})'
        elif months_worked > 0:
            duration = f' ({months_worked} {month_label})'

        return duration
