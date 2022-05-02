import logging

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework import status

from .logic.handleinmultipleaccounts import handleInMultipleAccounts
from .logic.utils import prependTimeAndSlug
from .logic.uploadtos3 import uploadToS3
from .constants import ERROR_MESSAGES

class FileUpload(APIView):
    parser_class = (FileUploadParser)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError(ERROR_MESSAGES.get('ContentMissing'))

        if not request.data.get('filename'):
            raise ParseError(ERROR_MESSAGES.get('NameMissing'))


        file = request.data.get('file')
        name = request.data.get('filename')
        filename = prependTimeAndSlug(name)

        requestIds = handleInMultipleAccounts(uploadToS3, file, filename)

        return Response(
            data={'data': requestIds},
            status=status.HTTP_201_CREATED,
        )
