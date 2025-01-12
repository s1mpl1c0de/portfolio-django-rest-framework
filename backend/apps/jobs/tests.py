from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.jobs.models import Experience


class JobAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(
            username='admin_user',
            email='admin@example.com',
            password='admin_password'
        )
        self.regular_user = User.objects.create_user(
            username='regular_user',
            email='regular@example.com',
            password='regular_password'
        )
        self.experience1 = Experience.objects.create(
            job_title='Marketing Intern',
            description='',
            company_name='Branding Solutions Ltd.',
            started_month=9,
            ended_month=12,
            started_year=2019,
            ended_year=2019,
            is_still_in_role=False,
            created_at=timezone.now(),
            created_user=self.admin_user,
            user=self.admin_user
        )
        self.experience2 = Experience.objects.create(
            job_title='Research Assistant Intern',
            description='',
            company_name='University of Science and Tech',
            started_month=7,
            ended_month=9,
            started_year=2018,
            ended_year=2018,
            is_still_in_role=False,
            created_at=timezone.now(),
            created_user=self.admin_user,
            user=self.admin_user
        )

    def test_create_experience_by_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('experience-list')

        data = {
            'job_title': 'Software Developer Internship',
            'description': '',
            'company_name': 'Tech Solutions Co., Ltd.',
            'started_month': 6,
            'ended_month': 12,
            'started_year': 2019,
            'ended_year': 2019,
            'is_still_in_role': False
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        experience = Experience.objects.filter(job_title=data.get('job_title')).first()
        self.assertEqual(data.get('job_title'), experience.job_title)
        self.assertEqual(data.get('description'), experience.description)
        self.assertEqual(data.get('company_name'), experience.company_name)
        self.assertEqual(data.get('started_month'), experience.started_month)
        self.assertEqual(data.get('ended_month'), experience.ended_month)
        self.assertEqual(data.get('started_year'), experience.started_year)
        self.assertEqual(data.get('ended_year'), experience.ended_year)
        self.assertEqual(data.get('is_still_in_role'), experience.is_still_in_role)

    def test_create_experience_with_invalid_year_by_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('experience-list')

        data = {
            'job_title': 'Mechanical Engineer Trainee',
            'description': '',
            'company_name': 'Precision Engineering Group',
            'started_month': 1,
            'ended_month': 4,
            'started_year': 2022,
            'ended_year': 2021,
            'is_still_in_role': False
        }

        response = self.client.post(url, data, format='json')
        errors = response.data.get('errors')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(errors[0], 'Start year cannot be later than end year.')

    def test_create_experience_with_invalid_month_by_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('experience-list')

        data = {
            'job_title': 'Data Analyst Internship',
            'description': '',
            'company_name': 'DataWorks Inc.',
            'started_month': 7,
            'ended_month': 5,
            'started_year': 2020,
            'ended_year': 2020,
            'is_still_in_role': False
        }

        response = self.client.post(url, data, format='json')
        errors = response.data.get('errors')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(errors[0], 'Ended month cannot be earlier than started month.')

    def test_create_experience_with_still_in_role_by_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('experience-list')

        data = {
            'job_title': 'Electrical Engineer Intern',
            'description': '',
            'company_name': 'PowerGrid Systems Ltd.',
            'started_month': 3,
            'ended_month': 6,
            'started_year': 2018,
            'ended_year': 2018,
            'is_still_in_role': True
        }

        response = self.client.post(url, data, format='json')
        errors = response.data.get('errors')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(errors[0], 'If still in role, ended year and ended month must not be provided.')

    def test_create_experience_with_not_still_in_role_by_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('experience-list')

        data = {
            'job_title': 'Civil Engineer Internship',
            'description': '',
            'company_name': 'Urban Developers Corp.',
            'started_month': 4,
            'ended_month': None,
            'started_year': 2017,
            'ended_year': None,
            'is_still_in_role': False
        }

        response = self.client.post(url, data, format='json')
        errors = response.data.get('errors')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(errors[0], 'If not still in role, both ended year and ended month must be provided.')

    def test_create_experience_by_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('experience-list')

        data = {
            'job_title': 'Graphic Designer Trainee',
            'description': '',
            'company_name': 'Creative Studio Ltd.',
            'started_month': 2,
            'ended_month': 5,
            'started_year': 2022,
            'ended_year': 2022,
            'is_still_in_role': False
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_experience_by_anonymous(self) -> None:
        url = reverse('experience-list')

        data = {
            'job_title': 'IT Support Internship',
            'description': '',
            'company_name': 'Global IT Services Co.',
            'started_month': 8,
            'ended_month': 10,
            'started_year': 2020,
            'ended_year': 2020,
            'is_still_in_role': False
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_experiences_by_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('experience-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)

    def test_get_all_experiences_by_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('experience-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)

    def test_get_all_experiences_by_anonymous(self) -> None:
        url = reverse('experience-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)

    def test_get_an_experience_by_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('experience-detail', kwargs={'uuid': self.experience1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_an_experience_by_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('experience-detail', kwargs={'uuid': self.experience1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_an_experience_by_anonymous(self) -> None:
        url = reverse('experience-detail', kwargs={'uuid': self.experience1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_experience_by_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('experience-detail', kwargs={'uuid': self.experience1.uuid})

        data = {
            'job_title': 'Product Manager Internship',
            'description': '',
            'company_name': 'InnovateTech Inc.',
            'started_month': 3,
            'ended_month': 5,
            'started_year': 2021,
            'ended_year': 2021,
            'is_still_in_role': False
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        experience = Experience.objects.filter(uuid=self.experience1.uuid).first()
        self.assertEqual(data.get('job_title'), experience.job_title)
        self.assertEqual(data.get('description'), experience.description)
        self.assertEqual(data.get('company_name'), experience.company_name)
        self.assertEqual(data.get('started_month'), experience.started_month)
        self.assertEqual(data.get('ended_month'), experience.ended_month)
        self.assertEqual(data.get('started_year'), experience.started_year)
        self.assertEqual(data.get('ended_year'), experience.ended_year)
        self.assertEqual(data.get('is_still_in_role'), experience.is_still_in_role)

    def test_update_experience_by_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('experience-detail', kwargs={'uuid': self.experience1.uuid})

        data = {
            'job_title': 'UX/UI Designer Intern',
            'description': '',
            'company_name': 'DesignHub Studios',
            'started_month': 1,
            'ended_month': 4,
            'started_year': 2022,
            'ended_year': 2022,
            'is_still_in_role': False
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_experience_by_anonymous(self) -> None:
        url = reverse('experience-detail', kwargs={'uuid': self.experience1.uuid})

        data = {
            'job_title': 'Digital Marketing Intern',
            'description': '',
            'company_name': 'MarketVision Ltd.',
            'started_month': 9,
            'ended_month': 12,
            'started_year': 2020,
            'ended_year': 2020,
            'is_still_in_role': False
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_experience_by_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('experience-detail', kwargs={'uuid': self.experience1.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_experience_by_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('experience-detail', kwargs={'uuid': self.experience1.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_experience_by_anonymous(self) -> None:
        url = reverse('experience-detail', kwargs={'uuid': self.experience1.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
