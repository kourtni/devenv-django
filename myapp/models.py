import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """Return True if the question was published within the last day."""
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    last_vote = models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, 0, 0))
    
    def __str__(self):
        return self.choice_text
    
    def vote(self):
        """Vote for this choice."""
        self.votes += 1
        self.last_vote = timezone.now()
        self.save()