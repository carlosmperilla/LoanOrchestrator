from django.test import TestCase
from .models import Applicant, LoanRequest

class ApplicantModelTest(TestCase):
    def setUp(self):
        self.applicant = Applicant.objects.create(
            dni='12345678',
            first_name='John',
            last_name='Doe',
            gender='M',
            email='john.doe@example.com'
        )

    def test_applicant_creation(self):
        self.assertTrue(isinstance(self.applicant, Applicant))
        self.assertEqual(self.applicant.__str__(), 'John Doe')

    def test_applicant_fields(self):
        self.assertEqual(self.applicant.dni, '12345678')
        self.assertEqual(self.applicant.first_name, 'John')
        self.assertEqual(self.applicant.last_name, 'Doe')
        self.assertEqual(self.applicant.gender, 'M')
        self.assertEqual(self.applicant.email, 'john.doe@example.com')

class LoanRequestModelTest(TestCase):
    def setUp(self):
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

    def test_loan_request_creation(self):
        self.assertTrue(isinstance(self.loan_request, LoanRequest))
        self.assertEqual(self.loan_request.__str__(), 'John Doe - 1000.0')

    def test_loan_request_fields(self):
        self.assertEqual(self.loan_request.amount, 1000.0)
        self.assertEqual(self.loan_request.approved, False)
        self.assertEqual(self.loan_request.applicant, self.applicant)
