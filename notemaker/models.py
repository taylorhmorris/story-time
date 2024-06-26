from datetime import timedelta
from django.conf import settings

from django.db import models
from django.utils import timezone

class Note(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
    )
    language = models.CharField(max_length=10, default='fr')
    word = models.CharField(max_length=50)
    ipa = models.CharField(max_length=50, blank=True)
    grammar = models.CharField(max_length=50, blank=True)
    definition = models.CharField(max_length=200, blank=True)
    example = models.CharField(max_length=200, blank=True)
    expression = models.CharField(max_length=200, blank=True)
    expression_meaning = models.CharField(max_length=200, blank=True)
    image = models.TextField(blank=True)
    
    def __str__(self):
        return self.word
    
    def get_dict(self):
        return {'word': self.word,
                'ipa': self.ipa,
                'grammar': self.grammar,
                'definition': self.definition,
                'example': self.example,
                'expression': self.expression,
                'expression_meaning': self.expression_meaning,
                'image': self.image,
                'owner': self.owner,
                'id': self.id}
    
class SearchResult(models.Model):
    word = models.CharField(max_length=50, unique=True)
    data = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=5, default='fr')
    
    def __str__(self):
        return self.word

class CardType(models.Model):
    card_type_name = models.CharField(max_length=30)
    
    @property
    def name(self):
        return self.card_type_name
    
    def __str__(self):
        return self.card_type_name
    
class CardManager(models.Manager):
    def are_due(self, owner):
        cards = Card.objects.filter(note__owner_id=owner.id, due_date__lte=timezone.now()).order_by('due_date','note')
        return cards
    
    def reset(self, owner):
        cards = Card.objects.filter(note__owner_id=owner.id)
        count = len(cards)
        for card in cards:
            card.reset()
        return count
    
class Card(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)
    due_date = models.DateTimeField(default=timezone.now)
    success = models.IntegerField(default=0)
    failure = models.IntegerField(default=0)
    fails_in_a_row = models.IntegerField(default=0)
    success_in_a_row = models.IntegerField(default=0)
    
    objects = models.Manager()
    custom_objects = CardManager()
    
    def __str__(self):
        return f"{self.note} - {self.card_type}"
    
    def get_dict(self):
        return {'id': self.id, 'card_type': self.card_type.name,
                'due_date': self.due_date,
                'note': self.note.get_dict()}
    
    def is_due(self):
        return self.due_date <= timezone.now()
        
    def schedule(self):
        srs = [0, 10, 24*60, 4*24*60, 8*24*60, 15*24*60, 30*24*60, 90*24*60]
        if self.success_in_a_row < len(srs):
            td = timedelta(minutes=srs[self.success_in_a_row])
        else:
            td = timedelta(minutes=srs[-1]*(2+self.success_in_a_row-len(srs)))
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
