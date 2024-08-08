
from typing import Any
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from secretkey.models import SecretKey
from managemodel.prediction import Prediction
from monitoring.models import NotAnsweredQuestion,QuestionMonitor
import datetime

# Create your views here.

class ChatbotAPI(APIView):
    
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.prediction_model = Prediction()
    
    def post(self,request):
        secret_key = get_authorization_header(request).decode('utf-8')
        model = SecretKey.objects.filter(secret_key=secret_key).first()
        current_date = datetime.datetime.now()
        if model:
            try:
                if model.status:
                    question = request.data.get('question')
                    answer,check = self.prediction_model.get_answer(question)
                    # return Response({'answer':answer}, status=status.HTTP_200_OK)
                    if check==True:
                        try:
                            question_monitor = QuestionMonitor.objects.filter(created_at=current_date).first()
                            if question_monitor:
                                question_monitor.answered += 1
                                question_monitor.save()
                            else:
                                QuestionMonitor.objects.create(answered=1,unanswered=0)
                        except QuestionMonitor.DoesNotExist:
                            return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
                            
                        return Response({'answer':answer}, status=status.HTTP_200_OK)
                    else:
                        NotAnsweredQuestion.objects.create(question=question,answer='No Answer')
                        try:
                            question_monitor = QuestionMonitor.objects.filter(created_at=current_date).first()
                            if question_monitor:
                                question_monitor.unanswered += 1
                                question_monitor.save()
                            else:
                                QuestionMonitor.objects.create(answered=0,unanswered=1)
                        except QuestionMonitor.DoesNotExist:
                            return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
                        return Response({'answer':answer}, status=status.HTTP_200_OK)
            except SecretKey.DoesNotExist:
                return Response({'error':'Secret Key is Inactive'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'Invalid Secret Key'}, status=status.HTTP_400_BAD_REQUEST)
        