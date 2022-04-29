from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework import status

class FileUpload(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        if not request.data.get('filename'):
            raise ParseError("Filename missing")

        file = request.data.get('file')
        filename = request.data.get('file')

        return Response(status=status.HTTP_201_CREATED)