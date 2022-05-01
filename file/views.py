import time
import logging

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework import status


from .s3 import uploadToMultipleAccounts

class FileUpload(APIView):
    parser_class = (FileUploadParser)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError('Empty content')

        if not request.data.get('filename'):
            raise ParseError('Filename missing')

        try:
            file = request.data.get('file')
            name = request.data.get('filename')

            requestIds = uploadToMultipleAccounts(file, name)

            return Response(
                data={'data': requestIds},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logging.error(e)

            return Response(
                data={'message': 'Something went wrong'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
