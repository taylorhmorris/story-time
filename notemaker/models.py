from datetime import timedelta, datetime

from django.db import models
from django.utils import timezone

class Note(models.Model):
    word = models.CharField(max_length=50)
    ipa = models.CharField(max_length=50, blank=True)
    grammar = models.CharField(max_length=50, blank=True)
    definition = models.CharField(max_length=50, blank=True)
    example = models.CharField(max_length=50, blank=True)
    expression = models.CharField(max_length=50, blank=True)
    expression_meaning = models.CharField(max_length=50, blank=True)
    image = models.TextField(blank=True)
    
    def __str__(self):
        return self.word
    
class SearchResult(models.Model):
    word = models.CharField(max_length=50, unique=True)
    data = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.word

class CardType(models.Model):
    card_type_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.card_type_name
    
class Card(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)
    due_date = models.DateTimeField(default=datetime.now)
    success = models.IntegerField(default=0)
    failure = models.IntegerField(default=0)
    fails_in_a_row = models.IntegerField(default=0)
    success_in_a_row = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.note} - {self.card_type}"
    
    def schedule(self):
        srs = [0, 15, 12*60, 24*60, 48*60, 5*24*60, 10*24*60]
        if self.success_in_a_row < len(srs):
            td = timedelta(minutes=srs[self.success_in_a_row])
        else:
            td = timedelta(minutes=srs[-1]*(self.success_in_a_row-len(srs)))
        print(f"{td} + {self.due_date} = {self.due_date + td}")
        self.due_date = timezone.now() + td
        self.save()
        return (td, self.due_date)
    
    def reset(self):
        self.success = 0
        self.failure = 0
        self.success_in_a_row = 0
        self.fails_in_a_row = 0
        self.due_date = timezone.now()
        self.save()
