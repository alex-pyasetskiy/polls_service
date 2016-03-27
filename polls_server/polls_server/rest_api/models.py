from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now=True)
    
    def __str__(self):
        return self.question


class Choice(models.Model):
    question = models.ForeignKey(Question, null=True, related_name="choices")
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice