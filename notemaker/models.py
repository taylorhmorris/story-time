from datetime import timedelta
from django.db import models

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
    due_date = models.DateTimeField(auto_now=True)
    success = models.IntegerField(default=0)
    failure = models.IntegerField(default=0)
    fails_in_a_row = models.IntegerField(default=0)
    success_in_a_row = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.note} - {self.card_type}"
    
    def set_due_date(self):
        self.due_date += timedelta(days=self.success_in_a_row*1)
