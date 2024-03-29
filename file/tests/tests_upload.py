import re
from unittest import mock

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from ..constants import ERROR_MESSAGES

class TestFile(APITestCase):
    url = reverse('file:upload')
    filename = 'image.jpeg'
    file = SimpleUploadedFile(filename, b'file_content', content_type='image/jpeg')

    @mock.patch('file.views.handleInMultipleAccounts', return_value=['REQID1', 'REQID2'])    
    def test_success_upload_endpoint(self, mock):
        requestIdRegex = r'[A-Z0-9]+'
        response = self.client.post(self.url, {
            'file': self.file,
            'filename': self.filename,
        })

        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(
            all(re.fullmatch(requestIdRegex, reqId)
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
