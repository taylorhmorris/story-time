import logging

from notemaker.utils.get_search_result import get_search_result, set_defaults
from .forms import NoteForm

from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Note, Card, CardType

class IndexView(TemplateView):
    template_name = "notemaker/index.html"

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

class NoteUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Note
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('notemaker:htmx-review-card')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
    
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

class CardListView(LoginRequiredMixin, ListView):
    model = Card

    def get_queryset(self):
        return self.model.objects.filter(note__owner_id=self.request.user.id)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "notemaker/dashboard.html"
    
 
@login_required
def htmx_generate_note(request):
    logger = logging.getLogger("view:htmx_generate_note")
    logger.setLevel(logging.DEBUG)
    if request.method == "POST":
        form = NoteForm(request.POST)
        logger.info(form.errors)
        if form.is_valid():
            if form.cleaned_data['owner'] != request.user:
                logger.debug(f'Invalid Card Creation attempted by {request.user} (pretending to be {form.cleaned_data["owner"]})')
                return render(request, "notemaker/utils/message.html", { "message": 'Invalid Owner' })
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
    logger = logging.getLogger("view:htmx_rate_card_view")
    card = Card.objects.get(pk=pk)
    if card.note.owner != request.user:
        logger.debug(f'Invalid Card Rating attempted by {request.user} on card #{card.id} (owned by {card.note.owner})')
        return htmx_review_card(request)
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
    logger = logging.getLogger("view:htmx_skip_card_view")
    card = Card.objects.get(pk=pk)
    if card.note.owner != request.user:
        logger.debug(f'Invalid Card Skip attempted by {request.user} on card #{card.id} (owned by {card.note.owner})')
        return htmx_review_card(request)
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
    logger = logging.getLogger("view:ajax_delete_card_view")
    card_id = request.GET.get('card_id', None)
    card = Card.objects.get(pk=card_id)
    try:
        note = card.note
        if note.owner != request.user:
            logger.debug(f'Invalid Card Delete attempted by {request.user} on card owned by {card.note.owner}')
            data = {'success': 'false', 'result': f'Permission Denied'}
        else:
            card.delete()
            data = {'success': 'true', 'result': f'Card {card_id} was deleted'}
    except:
        data = {'success': 'false', 'result': f'Card {card_id} could not be deleted due to an unknown error.'}
    return JsonResponse(data)

@login_required
def card_detail_view(request, pk):
    logger = logging.getLogger("view:card_detail_view")
    logger.setLevel(logging.DEBUG)
    card_obj = Card.objects.get(pk=pk)
    if card_obj.note.owner != request.user:
        logger.debug(f'Invalid CardDetailView attempted by {request.user} on card owned by {card_obj.note.owner}')
        return render(request, "notemaker/utils/message.html", { "message": "Forbidden" })
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
    
