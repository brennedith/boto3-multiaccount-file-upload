import re

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from ..constants import ERROR_MESSAGES

# TODO: Mock s3 file upload

class TestsInfra(APITestCase):
    url = reverse('file:upload')
    filename = 'image.jpeg'
    file = SimpleUploadedFile(filename, b'file_content', content_type='image/jpeg')
    
    def test_success_upload_endpoint(self):
        s3RequestIdRegex = r'[A-Z0-9]+'

        response = self.client.post(self.url, {
            'file': self.file,
            'filename': self.filename,
        })

        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(
            all(re.fullmatch(s3RequestIdRegex, reqId)
            for reqId in response.data.get('data'))
        )


    def test_failure_upload_endpoint_file_missing(self):
        response = self.client.post(self.url, {
            'filename': self.filename,
        })

        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(response.data.get('detail'), ERROR_MESSAGES.get('ContentMissing'))


    def test_failure_upload_endpoint_filename_missing(self):
        response = self.client.post(self.url, {
            'file': self.file,
        })

        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(response.data.get('detail'), ERROR_MESSAGES.get('NameMissing'))
