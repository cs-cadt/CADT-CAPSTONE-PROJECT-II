from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from monitoring.models import NotAnsweredQuestion,QuestionMonitor
# Create your views here.
import pandas as pd
class UnAnsweredAPI(APIView):
    def get(self,request):
        unanswered = NotAnsweredQuestion.objects.all().values()
        return Response({'unanswered':unanswered}, status=status.HTTP_200_OK)
    def delete(self,request):
        id = request.query_params.get('id')
        model = NotAnsweredQuestion.objects.filter(id=id)
        if model:
            model.delete()
            return Response({'message':'Delete Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Delete Failed'}, status=status.HTTP_400_BAD_REQUEST)
        
def get_by(data_frame, date, type_response = "t",type="day"):
    try:
        if type_response=="a":
            return data_frame[data_frame[type]==date]["answered"].values[0]
        elif type_response=="u":
          return data_frame[data_frame[type]==date]["unanswered"].values[0]
        else:
          return data_frame[data_frame[type]==date]["total"].values[0]
    except:
        return 0
class QuestionMonitorAPI(APIView):
    def get(self,request):
        question_monitor = QuestionMonitor.objects.all().values()
        df = pd.DataFrame(question_monitor)
        df["total"] = df["answered"] + df["unanswered"]
        df["day"] = pd.to_datetime(df["created_at"]).dt.day_name()
        df["month"] = pd.to_datetime(df["created_at"]).dt.month_name()
        df = df.drop(columns=["created_at","id"])
        df_day = df.drop(columns=["month"]).groupby("day").sum().reset_index()
        df_month = df.drop(columns=["day"]).groupby("month").sum().reset_index()
        label_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        label_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        response = {
                    "week":{
                            'labels': label_days,
                            'datasets': [
                            {
                                'label': 'Total Request',
                                'data': [get_by(df_day, each_day,type_response="t",type="day") for each_day in label_days],
                                'backgroundColor': '#2C50C5',
                                'stack': 'Stack 0'
                            },
                            {
                                'label': 'Total Answered',
                                'data': [get_by(df_day, each_day,type_response="a",type="day") for each_day in label_days],
                                'backgroundColor': '#5577E3',
                                'stack': 'Stack 0'
                            },
                            {
                                'label': 'Total Unanswered',
                                'data': [get_by(df_day, each_day,type_response="u",type="day") for each_day in label_days],
                                'backgroundColor': '#9CC8FF',
                                'stack': 'Stack 0'
                            }
                            ]
                        },
                    "month":{
                            'labels': label_months,
                            'datasets': [
                            {
                                'label': 'Total Request',
                                'data': [get_by(df_month, each_month,type_response="t",type="month") for each_month in label_months],
                                'backgroundColor': '#2C50C5',
                                'stack': 'Stack 0'
                            },
                            {
                                'label': 'Total Answered',
                                'data': [get_by(df_month, each_month,type_response="a",type="month") for each_month in label_months],
                                'backgroundColor': '#5577E3',
                                'stack': 'Stack 0'
                            },
                            {
                                'label': 'Total Unanswered',
                                'data': [get_by(df_month, each_month,type_response="u",type="month") for each_month in label_months],
                                'backgroundColor': '#9CC8FF',
                                'stack': 'Stack 0'
                            }
                            ]
                        }
                    }
        return Response(response, status=status.HTTP_200_OK)