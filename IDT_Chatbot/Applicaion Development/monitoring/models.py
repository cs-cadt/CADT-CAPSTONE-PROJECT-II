from django.db import models

# Create your models here.
class NotAnsweredQuestion(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class QuestionMonitor(models.Model):
    answered = models.IntegerField(default=8)
    unanswered = models.IntegerField(default=8)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.question