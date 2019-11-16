'''
file upload && download
'''

import os
import uuid as uuid_utils
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from django.conf import settings
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from common.minio_utils import (
    put_object,
    presign_get,
)


class FileCreateAPIView(generics.CreateAPIView):
    '''
    upload a file
    '''

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''
        upload file
        '''
        file = request.data.get('file')
        uuid = uuid_utils.uuid4().hex
        suffix = os.path.splitext(file.name)[1]
        file_name = uuid + suffix
        try:
            put_object(
                bucket_name=settings.MINIO_BUCKET,
                object_name=file_name,
                file_data=file,
                length=file.size,
            )
        except Exception:    # pylint: disable=broad-except
            with open(settings.UPLOADFILES_PATH + file_name, 'wb') as f:
                f.write(file.read())
        return Response({'file_name': file_name})


class FileAPIView(View):
    '''
    download the file
    '''

    permission_classes = []
    authentication_classes = []

    def get(self, request, uuid):    # pylint: disable=unused-argument, no-self-use
        '''
        download file
        '''
        try:
            url = presign_get(bucket_name=settings.MINIO_BUCKET,
                              object_name=uuid,
                              response_headers={
                                  'response-content-disposition': 'attachment;filename=%s' % uuid,
                              })
            return HttpResponseRedirect(url)
        except Exception:    # pylint: disable=broad-except
            data = ''
            if os.path.exists(settings.UPLOADFILES_PATH + uuid):
                data = open(settings.UPLOADFILES_PATH + uuid, 'rb').read()
                return HttpResponse(data)
            return Response(data, HTTP_404_NOT_FOUND)
