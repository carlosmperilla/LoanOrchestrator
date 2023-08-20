from urllib.parse import urlparse
from decimal import Decimal as D

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from loanservice.models import Applicant, LoanRequest

class LoanRequestViewSetTest(TestCase):
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
        self.loan_request = LoanRequest.objects.create(
            amount=1000.0,
            approved=False,
            applicant=self.applicant
        )

    def test_loan_request_list(self):
        url = reverse('loanrequest-list')
        response_nostaff = self.client_nostaff.get(url)
        response_staff = self.client_staff.get(url)
        self.assertEqual(response_nostaff.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_staff.status_code, status.HTTP_200_OK)
        self.assertEqual(response_staff.json().get('count'), 1)

    def test_loan_request_retrieve(self):
        url = reverse('loanrequest-detail', args=[self.loan_request.slug])
        response_nostaff = self.client_nostaff.get(url)
        response_staff = self.client_staff.get(url)

        url_applicant = response_staff.data['applicant']
        parsed_url = urlparse(url_applicant)
        path_parts = parsed_url.path.strip('/').split('/')
        slug = path_parts[-1]

        self.assertEqual(response_nostaff.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_staff.status_code, status.HTTP_200_OK)
        self.assertEqual(response_staff.data['amount'], '1000.00')
        self.assertAlmostEqual(float(response_staff.data['amount']), float('1000.0'))
        self.assertEqual(slug, str(self.applicant.slug))

    def test_loan_request_create(self):
        url = reverse('loanrequest-list')
        applicant_url = reverse('applicant-detail', args=[self.applicant.slug])
        data_one = {
            'amount': 2000.0,
            'applicant': applicant_url
        }
        data_two = {
            'amount': 2010.0,
            'applicant': applicant_url
        }
        response_nostaff = self.client_nostaff.post(url, data_one)
        response_staff = self.client_staff.post(url, data_two)
        self.assertEqual(response_nostaff.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_staff.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoanRequest.objects.count(), 3)

    def test_loan_request_update(self):
        url = reverse('loanrequest-detail', args=[self.loan_request.slug])
        applicant_url = reverse('applicant-detail', args=[self.applicant.slug])
        data = {
            'amount': 2020.0,
            'applicant': applicant_url
        }
        response = self.client_staff.put(url, data)
        fail_response = self.client_nostaff.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(fail_response.status_code, status.HTTP_403_FORBIDDEN)
        self.loan_request.refresh_from_db()
        self.assertEqual(self.loan_request.amount, D('2020.00'))
        self.assertAlmostEqual(float(self.loan_request.amount), float('2020.0'))
        self.assertEqual(self.loan_request.applicant, self.applicant)

    def test_loan_request_partial_update(self):
        url = reverse('loanrequest-detail', args=[self.loan_request.slug])
        data = {
            'amount': 3000.0
        }
        response = self.client_staff.patch(url, data)
        fail_response = self.client_nostaff.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(fail_response.status_code, status.HTTP_403_FORBIDDEN)
        self.loan_request.refresh_from_db()
        self.assertEqual(self.loan_request.amount, 3000.0)

    def test_loan_request_destroy(self):
        url = reverse('loanrequest-detail', args=[self.loan_request.slug])
        response = self.client_staff.delete(url)
        fail_response = self.client_nostaff.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(fail_response.status_code, status.HTTP_403_FORBIDDEN)
