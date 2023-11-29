import logging
import json
import base64
from random import shuffle
import requests

from notemaker.utils.get_search_result import get_search_result, set_defaults
from .forms import NoteForm

from thscraper.thscraper import query_all

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Note, SearchResult, Card, CardType

class IndexView(TemplateView):
    template_name = "notemaker/index.html"
    
class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    
class NoteUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Note
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('notemaker:htmx-review-card')

class NoteCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Note
    fields = '__all__'
    
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    
class CardListView(LoginRequiredMixin, ListView):
    model = Card

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "notemaker/dashboard.html"
    
@login_required
def create_note_form(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            return HttpResponse("Form submitted!")
    else:
        form = NoteForm({'word': 'testing'})
    return render(request, "notemaker/note_form.html", {"form": form})

@login_required
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
    
@login_required
def htmx_generate_note(request):
    logger = logging.getLogger("view:htmx_generate_note")
    logger.setLevel(logging.DEBUG)
    if request.method == "POST":
        form = NoteForm(request.POST)
        logger.info(form.errors)
        if form.is_valid():
            new_note = form.save(commit=True)
            i2w = CardType.objects.get(card_type_name="ImageToWord")
            Card(note=new_note, card_type=i2w).save()
            w2i = CardType.objects.get(card_type_name="WordToImage")
            Card(note=new_note, card_type=w2i).save()
            fitb = CardType.objects.get(card_type_name="FillInTheBlank")
            Card(note=new_note, card_type=fitb).save()
            return render(request, "notemaker/utils/message.html", { "message": 'Note created' })
        word = form.data['word']
        data = get_search_result(word)
        data_defaults = {
            "definition": form.data['definition'],
            "expression": [form.data['expression']],
            "expression_meaning": [form.data['expression_meaning']],
            "example": [form.data['example']],
            "image": [form.data['image']],
        }
        data = data | data_defaults
        return render(request, "notemaker/note_form.html", {"form": form, "data": data})
    else:
        word = request.GET.get('word', None)
        data = get_search_result(word)
        if not data:
            return render(request, "notemaker/utils/message.html", { "message": 'Error: could not collect note data' })
        data = set_defaults(data)
        data['owner'] = request.user.id
        try:
            form = NoteForm(data)
            form.word = data['word']
        except Exception as e:
            logger.error(e)
            return render(request, "notemaker/utils/message.html", { "message": 'Error: could not generate note card' })
    return render(request, "notemaker/note_form.html", {"form": form, "data": data})

@login_required
def htmx_rate_card_view(request, pk, rating):
    card = Card.objects.get(pk=pk)
    if rating == '0':
        card.failure += 1
        card.fails_in_a_row += 1
        card.success_in_a_row = 0
    elif rating == '-1':
        card.due_date = timezone.now()
        card.save()
    else:
        card.success += 1
        card.success_in_a_row += int(rating)
        card.fails_in_a_row = 0
    card.save()
    card.schedule()
    return htmx_review_card(request)

@login_required
def htmx_skip_card_view(request, pk):
    card = Card.objects.get(pk=pk)
    card.due_date = timezone.now()
    card.save()
    return htmx_review_card(request)

@login_required
def htmx_review_card(request):
    max_number = 1
    cards = Card.custom_objects.are_due(request.user)[:max_number]
    if len(cards) > 0:
        card_type_obj = CardType.objects.get(pk=cards[0].card_type.pk)
        context = { 'card': cards[0], 'template': card_type_obj.card_type_name }
        return render(request, "notemaker/card_detail.html", context)
    return render(request, "notemaker/utils/message.html", { "message": "No cards to review" })

@login_required
def ajax_delete_card_view(request):
    card_id = request.GET.get('card_id', None)
    card = Card.objects.get(pk=card_id)
    try:
        note = card.note
        assert note.owner == request.user
        card.delete()
        data = {'success': 'true', 'result': f'Card {card_id} was deleted'}
    except:
        data = {'success': 'false', 'result': f'Card {card_id} could not be deleted due to an unknown error.'}
    return JsonResponse(data)

@login_required
def card_detail_view(request, pk):
    card_obj = Card.objects.get(pk=pk)
    card_type_obj = CardType.objects.get(pk=card_obj.card_type.pk)
    context = {'card': card_obj,
               'template': card_type_obj.card_type_name}
    return render(request,
               "notemaker/card_detail.html",
               context)

@login_required
def api_view(request):
    #data = request.GET.get('data', None)
    request_type = request.GET.get('request', None)
    if request_type == 'reset':# and 'hard' in data['flags']:
        count = Card.custom_objects.reset(request.user)
        results = {'success': True, 'message': f'{count} cards reset'}
    else:
        results = {'success': False, 'message': 'Invalid Command'}
    return JsonResponse(results)
    
