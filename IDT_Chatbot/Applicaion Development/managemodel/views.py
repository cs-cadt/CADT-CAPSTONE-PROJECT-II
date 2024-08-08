from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os
from .training import TrainingModel
import time
from dotenv import set_key,dotenv_values
from .prediction import Prediction
# Create your views here.


def checkname(checking_path,name):
    list_file = os.listdir(checking_path)
    if name in list_file:
        return False
    return True


class ManageModelAPI(APIView):
    # list all the models
    def get(self,request):
        file_name = os.listdir('ds/models')
        return Response({'models':file_name}, status=status.HTTP_200_OK)
    

class ChangeModelAPI(APIView):
    # list all the models
    def get(self,request):
        file_name = os.listdir('ds/models')
        return Response({'models':file_name}, status=status.HTTP_200_OK)
    
    # change the model
    def post(self,request):
        model_name = request.data.get('modelname')
        if model_name:
            start_time = time.time()
            prediction = Prediction()
            set_key(".env","USE_MODEL",model_name)
            prediction.renew()
            end_time = time.time()
            total_time = end_time - start_time

            return Response({'message': 'Model has been changed.','time':total_time}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Model not found.'}, status=status.HTTP_404_NOT_FOUND)

class TrainModelAPI(APIView):
    def post(self,request):
        file_name = request.data.get('filename')
        model_name = request.data.get('modelname')
        if file_name and model_name:
            machine = TrainingModel(file_name,model_name)
            
            result = machine.train()
            if result:
                return Response({'message': 'Model has been trained, succefully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Model failed to train.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': "please provide data and set name of model"}, status=status.HTTP_400_BAD_REQUEST)


class RunningModelAPI(APIView):
    def get(self,request):
        model_name = dotenv_values(".env")['USE_MODEL']
        return Response({'model':model_name}, status=status.HTTP_200_OK)

class UploadModelAPI(APIView):
    def post(self,request):
        try:
            file = request.FILES.get('file')
            module_type = request.query_params.get('module_type') # model or setting
            if file:
                file_extension = file.name.split('.')[-1].lower()
                if file_extension != 'pkl':
                    return Response({'error': 'File type not supported. Please upload a pkl file.'}, status=status.HTTP_400_BAD_REQUEST)
                file_name = str(file.name).split('.')[0]+'.'+file_extension
                if module_type == 'model':
                    if checkname('ds/models',file_name) == False:
                        return Response({'error': 'Model already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                    file_path = f"ds/{module_type}s/{file_name}"
                else:
                    if checkname('ds/setting',file_name) == False:
                        return Response({'error': 'Setting already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                    file_path = f"ds/{module_type}/{file_name}"
                # directory = os.path.dirname(file_path)
                # os.makedirs(directory, exist_ok=True)
                start_time = time.time()
                with open(file_path,'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                end_time = time.time()
                total_time = end_time - start_time
                return Response({
                    'status':status.HTTP_200_OK,
                    'message':"Model has been uploaded successfully",
                    'upload_time': f"{total_time} seconds"
                },status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No file was uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'An error occured while uploading the model.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class DeleteModelAPI(APIView):
    def delete(self,request):
        file_name = request.query_params.get('filename')
        # module_type = request.query_params.get('module_type') # model or scaler
        file_path = f"ds/models/{file_name}.pkl"
        file_path_1 = f"ds/scalers/{file_name}.pkl"
        if os.path.exists(file_path) and os.path.exists(file_path_1):
            os.remove(file_path)
            os.remove(file_path_1)
            return Response({'message': 'model has been deleted.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'model not found.'}, status=status.HTTP_404_NOT_FOUND)
            
