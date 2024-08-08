from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core.mail import send_mail
import random
from .models import VerifyCode
from django.core.management.utils import get_random_secret_key
from rest_framework.authentication import get_authorization_header
from django.utils import timezone
# Create your views here.

class Auths(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username:
            user = authenticate(username=username,password=password)
            if user:
                user.last_login = timezone.now()
                user.save()
                token,created = Token.objects.get_or_create(user=user)
                return Response({
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'email':user.email,
                    'token':token.key,
                    'meta':{
                        'status':status.HTTP_200_OK,
                        'message':"User authenticated successfully",
                        'date': user.date_joined
                    }
                    
                    })
            else:
                return Response({
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'message':"username or password is invalid"
                    })
        else:
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':"username or password is invalid"
            })

class ForgotPasswordAPI(APIView):
    def post(self,request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if user:
                code = random.randint(100000,999999)
                model,created = VerifyCode.objects.get_or_create(email=email)
                model.code = code
                send_code(code,email)
                model.save()
                return Response({'message':'Email has been sent successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message':'Email is not found'}, status=status.HTTP_404_NOT_FOUND)

class VerifyCodeAPI(APIView):
    def post(self,request):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            model = VerifyCode.objects.get(email=email,code=code)
            if model:
                verify = get_random_secret_key()
                model.code = verify
                model.save()
                return Response({'message':'Code is correct','verify':verify}, status=status.HTTP_200_OK)
        except VerifyCode.DoesNotExist:
            return Response({'message':'Code is incorrect'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordAPI(APIView):
    def post(self,request):
        verify = get_authorization_header(request).decode('utf-8')
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            model = VerifyCode.objects.get(email=email,code=verify)
            print(model)
            if model:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                model.code = get_random_secret_key()
                model.save()
                return Response({'message':'Password has been reset successfully'}, status=status.HTTP_200_OK)
        except VerifyCode.DoesNotExist:
            return Response({'message':'Something went wrong!'}, status=status.HTTP_404_NOT_FOUND)

def send_code(code:int,email:str):
    subject = "Verify Code - Forgot Password"
    message = f"Here is verify code: {code}"
    email_from = 'IDT Chatbot <davannsmart9@gmail.com>'
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
