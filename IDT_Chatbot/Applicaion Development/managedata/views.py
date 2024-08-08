from django.core.management.utils import get_random_secret_key
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import time
import os
# Create your views here.

def checkname(checking_path,name):
    list_file = os.listdir(checking_path)
    if name in list_file:
        return False
    return True

class UploadFileAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    def get(self,request):
        file_list = os.listdir('data_storage')
        return Response({'files':file_list}, status=status.HTTP_200_OK)
    def delete(self,request):
        file_name = request.query_params.get('filename')
        file_path = f"data_storage/{file_name}"
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            return Response({'message': 'File has been deleted.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        file = request.FILES.get('file')
        if file:
            file_extension = file.name.split('.')[-1].lower()
            if file_extension != 'csv':
                return Response({'error': 'File type not supported. Please upload a CSV file.'}, status=status.HTTP_400_BAD_REQUEST)
            file_name = str(file.name).split('.')[0]+'_'+str(time.time())+'.'+file_extension
            file_path = f"data_storage/{file_name}"
            directory = os.path.dirname(file_path)
            os.makedirs(directory, exist_ok=True)
            start_time = time.time()
            with open(file_path,'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            end_time = time.time()
            total_time = end_time - start_time
            return Response({
                'status':status.HTTP_200_OK,
                'message':"File has been uploaded successfully",
                'upload_time': f"{total_time} seconds"
            },status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No file was uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

class downloadFileAPI(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]
    def get(self,request):
        file_name = request.query_params.get('filename')
        file_path = f"data_storage/{file_name}"
        print(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = Response(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename={file_name}'
                return response
        else:
            return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)