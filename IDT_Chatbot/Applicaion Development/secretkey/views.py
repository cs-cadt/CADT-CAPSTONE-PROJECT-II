from django.core.management.utils import get_random_secret_key
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import SecretKey
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
# Create your views here.

class SecretKeyAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def post(self,request):
        name = request.data.get('name')
        key = get_random_secret_key()
        model = SecretKey.objects.create(name=name,secret_key=key)
        if model:
            return Response({
                'id':model.id,
                'name':name,
                'secret_key':key,
                'meta':{
                    'status':status.HTTP_200_OK,
                    'message':"Secret key has been saved successfully"
                 }
            })
        else:
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':"Something is invalid"
            })
    def get(self,request):
        secret_keys = SecretKey.objects.all()
        return Response(secret_keys.values())
    
    def delete(self,request):
        id = int(request.data.get('id'))
        model = SecretKey.objects.filter(id=id)
        
        if model:
            name = model.first().name + ""
            model.delete()
            return Response({
                'name':name,
                'meta':{
                    'status':status.HTTP_200_OK,
                    'message':"Secret key has been deleted successfully"
                 }
            })
        else:
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':"Something is invalid"
            })
            
    def put(self,request):
        id = int(request.data.get('id'))
        name = request.data.get('name')
        model = SecretKey.objects.filter(id=id).first()
        old_name = model.name + ""
        model.name = name
        if model:
            model.save()
            return Response({
                'old_name':old_name,
                'new_name':model.name,
                'meta':{
                    'status':status.HTTP_200_OK,
                    'message':"Secret key has been updated successfully"
                 }
            })
        else:
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':"Something is invalid"
            })