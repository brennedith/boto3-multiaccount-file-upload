import time
import random, string

import environ
import boto3
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework import status

env = environ.Env()

session = boto3.Session(
    aws_access_key_id=env('AWS_ACCESS_KEY_ID_A'),
    aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY_A'),
    region_name='us-west-2',
)
s3 = session.resource('s3')

def randomword(length = 8):
   letters = string.ascii_letters
   return ''.join(random.choice(letters) for i in range(length))

class FileUpload(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError('Empty content')

        if not request.data.get('filename'):
            raise ParseError('Filename missing')

        file = request.data.get('file')
        name = request.data.get('file')

        random_slug = randomword()
        timestamp = str(int(time.time()))
      
        filename_list = [timestamp, random_slug, name]
        filename = '-'.join(str(x) for x in filename_list)

        s3.Bucket('mentum01').put_object(Key=filename, Body=file)

        return Response(status=status.HTTP_201_CREATED)