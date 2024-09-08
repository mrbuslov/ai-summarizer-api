import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class SummarizePDFTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('summarize-pdf')

    def generate_test_pdf(self):
        """Helper method to create a simple PDF in memory."""
        # TODO: create file in memory instead of on disk. This is temp solution.
        pdf_path = os.path.join(os.path.dirname(__file__) + '/materials/.', 'file_test.pdf')
        with open(pdf_path, 'rb') as pdf_file:
            return SimpleUploadedFile(
                name='file_text.pdf',
                content=pdf_file.read(),
                content_type='application/pdf'
            )

    def test_summarize_pdf_with_valid_pdf(self):
        """Test uploading a valid PDF file and receiving a summary."""
        pdf_file = self.generate_test_pdf()
        response = self.client.post(self.url, {'file': pdf_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary', response.data)

    def test_summarize_pdf_without_file(self):
        """Test uploading without a file and receiving an error."""
        response = self.client.post(self.url, {}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
