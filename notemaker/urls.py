from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('fake/', views.FakeWebsiteView.as_view(), name='fake_website'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
    path('note/', views.NoteListView.as_view(), name='note-list'),
    path('card/<int:pk>/', views.card_detail_view, name='card-detail'),
    path('card/', views.CardListView.as_view(), name='card-list'),
    
    path('ajax/testing/', views.test_ajax, name='test_ajax'),
    path('ajax/anki_generate_note/', views.ajax_anki_generate_note, name='ajax_anki_generate_note'),
    path('ajax/anki_create_note/', views.ajax_anki_create_note, name='ajax_anki_create_note'),
    path('ajax/get_note/', views.ajax_note_detail_view, name='ajax-note-detail'),
    path('ajax/rate_card/', views.ajax_rate_card_view, name='ajax-rate-card'),
    
]
