from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from loanservice.models import Applicant

class ApplicantViewSetTest(TestCase):
    def setUp(self):
        self.client_nostaff = APIClient()
        self.client_staff = APIClient()
        self.user_nostaff = User.objects.create_user(username='testuser_nostaff', password='testpass')
        self.user_staff = User.objects.create_user(username='testuser_staff', password='testpass', is_staff=True)
        self.client_nostaff.login(username='testuser_nostaff', password='testpass')
        self.client_staff.login(username='testuser_staff', password='testpass')
        self.applicant = Applicant.objects.create(
            dni='12345678',
            first_name='John',
            last_name='Doe',
            gender='M',
            email='john.doe@example.com'
        )

    def test_applicant_list(self):
        url = reverse('applicant-list')
        response_nostaff = self.client_nostaff.get(url)
        response_staff = self.client_staff.get(url)
        self.assertEqual(response_nostaff.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_staff.status_code, status.HTTP_200_OK)
        self.assertEqual(response_staff.json().get('count'), 1)

    def test_applicant_retrieve(self):
        url = reverse('applicant-detail', args=[self.applicant.slug])
        response_nostaff = self.client_nostaff.get(url)
        response_staff = self.client_staff.get(url)
        self.assertEqual(response_nostaff.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_staff.status_code, status.HTTP_200_OK)
        self.assertEqual(response_staff.data['dni'], '12345678')
        self.assertEqual(response_staff.data['first_name'], 'John')
        self.assertEqual(response_staff.data['last_name'], 'Doe')
        self.assertEqual(response_staff.data['gender'], 'M')
        self.assertEqual(response_staff.data['email'], 'john.doe@example.com')

    def test_applicant_create(self):
        url = reverse('applicant-list')
        data_one = {
            'dni': '87654321',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'gender': 'F',
            'email': 'jane.doe@example.com'
        }
        data_two = {
            'dni': '88654321',
            'first_name': 'Joe',
            'last_name': 'Smith',
            'gender': 'O',
            'email': 'joe.smith@example.com'
        }
        response_nostaff = self.client_nostaff.post(url, data_one)
        response_nostaff_repeat = self.client_nostaff.post(url, data_one)
        response_staff = self.client_staff.post(url, data_two)
        response_staff_repeat = self.client_staff.post(url, data_two)
        self.assertEqual(response_nostaff.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_staff.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_nostaff_repeat.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_staff_repeat.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Applicant.objects.count(), 3)

    def test_applicant_update(self):
        url = reverse('applicant-detail', args=[self.applicant.slug])
        data = {
            'dni': '87654321',
            'first_name': 'Julia',
            'last_name': 'Doe',
            'gender': 'F',
            'email': 'jane.doe@example.com'
        }
        response = self.client_staff.put(url, data)
        fail_response = self.client_nostaff.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(fail_response.status_code, status.HTTP_403_FORBIDDEN)
        self.applicant.refresh_from_db()
        self.assertEqual(self.applicant.dni, '87654321')
        self.assertEqual(self.applicant.first_name, 'Julia')
        self.assertEqual(self.applicant.last_name, 'Doe')
        self.assertEqual(self.applicant.gender, 'F')
        self.assertEqual(self.applicant.email, 'jane.doe@example.com')

    def test_applicant_partial_update(self):
        url = reverse('applicant-detail', args=[self.applicant.slug])
        data = {
            'first_name': 'Janice'
        }
        response = self.client_staff.patch(url, data)
        fail_response = self.client_nostaff.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(fail_response.status_code, status.HTTP_403_FORBIDDEN)
        self.applicant.refresh_from_db()
        self.assertEqual(self.applicant.first_name, 'Janice')

    def test_applicant_destroy(self):
        url = reverse('applicant-detail', args=[self.applicant.slug])
        response = self.client_staff.delete(url)
        fail_response = self.client_nostaff.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(fail_response.status_code, status.HTTP_403_FORBIDDEN)