from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes, smart_text, smart_bytes
from django.core import serializers

import json
from bs4 import BeautifulSoup
import base64
import requests
from PIL import Image
from io import StringIO
import html

import thscraper
from pprint import pprint as pp

from .models import Note, SearchResult, Card, CardType

class IndexView(TemplateView):
    template_name = "notemaker/index.html"
    
class FakeWebsiteView(TemplateView):
    template_name = "notemaker/fake.html"
    
class NoteDetailView(DetailView):
    model = Note
    
class NoteListView(ListView):
    model = Note
    
class CardListView(ListView):
    model = Card
    
def test_ajax(request):
    rec = request.GET.get('rec', None)
    data = {
        'result': f"You sent us: {rec}, and now we're sending it back to you."
    }
    return JsonResponse(data)

def deserialize(serial):
    results = dict()
    if len(serial) == 0:
        return results
    try:
        items = serial.split('&')
    except ValueError:
        items = [serial]
    for item in items:
        key, value = item.split("=")
        #if key in results:
        #    results[key].append(value)
        #else:
        #    results[key] = [value]
        results[key] = value
    return results
    

def ajax_anki_create_note(request):
    word = request.GET.get('word', None)
    form = deserialize(request.GET.get('form', None))
    
    sr = SearchResult.objects.values_list('data', flat=True).get(word=word)
    sr_data = json.decoder.JSONDecoder().decode(sr)
    
    new_note = Note(word=word)
    
    new_note.ipa = sr_data['ipa']
    new_note.grammar = sr_data['grammar']
    new_note.definition = sr_data['definitions'][int(form['def'])]['definition']
    new_note.example = sr_data['examples'][int(form['example'])]['source']
    new_note.expression = sr_data['expressions'][int(form['expression'])]['expression']
    new_note.expression_meaning = sr_data['expressions'][int(form['expression'])]['definition']
    new_note.image = sr_data['images'][int(form['selectedImg'])]
    new_note.save()
    
    i2w = CardType.objects.get(card_type_name="ImageToWord")
    Card(note=new_note, card_type=i2w).save()
        
    w2i = CardType.objects.get(card_type_name="WordToImage")
    Card(note=new_note, card_type=w2i).save()
    
    data = {
        'note_id': new_note.id,
        }
    
    return JsonResponse(data)

def ajax_anki_generate_note(request):
    word = request.GET.get('word', None)
    
    try:
        sr = SearchResult.objects.values_list('data', flat=True).get(word=word)
        data = json.decoder.JSONDecoder().decode(sr)
    except:
        print(f"No Saved Result. Asking thscraper for {word}")
        data = thscraper.query_all(word)
        b64images = [base64.b64encode(requests.get(img).content).decode()
                     for img in data['images']]
        data['images'] = b64images
        new_search = SearchResult(word=word)
        new_search.data = json.dumps(data)
        new_search.save()
    context = {'data': data}
    #return JsonResponse(data)
    return render(request, "notemaker/note_create.html", context)

def ajax_note_detail_view(request):
    note_id = request.GET.get('note_id', None)
    context = {'note': Note.objects.get(pk=note_id)}
    return render(request, "notemaker/note_detail.html", context)

def ajax_rate_card_view(request):
    card_id = request.GET.get('card_id', None)
    card = Card.objects.get(pk=card_id)
    rating = request.GET.get('rating', None)
    if rating == '0':
        card.failure += 1
        card.fails_in_a_row += 1
        card.success_in_a_row = 0
    else:
        card.success += 1
        card.success_in_a_row += int(rating)
        card.fails_in_a_row = 0
    card.save()
    new_date = card.schedule()
    data = {'success': 'true', 'new_date': new_date}
    return JsonResponse(data)

def card_detail_view(request, pk):
    card_obj = Card.objects.get(pk=pk)
    card_type_obj = CardType.objects.get(pk=card_obj.card_type.pk)
    context = {'card': card_obj,
               'template': card_type_obj.card_type_name}
    return render(request,
               "notemaker/card_detail.html",
               context)
