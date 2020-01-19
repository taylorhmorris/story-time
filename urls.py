from django.urls import path

from . import views

app_name = 'notemaker'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
    path('note/', views.NoteListView.as_view(), name='note-list'),
    path('card/<int:pk>/', views.card_detail_view, name='card-detail'),
    path('card/', views.CardListView.as_view(), name='card-list'),
    
    path('workshop/', views.WorkshopView.as_view(), name='workshop'),
    
    path('ajax/testing/', views.test_ajax, name='test_ajax'),
    path('ajax/anki_generate_note/', views.ajax_anki_generate_note, name='ajax_anki_generate_note'),
    path('ajax/anki_create_note/', views.ajax_anki_create_note, name='ajax_anki_create_note'),
    path('ajax/get_note/', views.ajax_note_detail_view, name='ajax-note-detail'),
    path('ajax/rate_card/', views.ajax_rate_card_view, name='ajax-rate-card'),
    path('ajax/card_detail/', views.ajax_card_detail_view, name='ajax-card-detail'),
    path('ajax/review/', views.ajax_review_cards, name='ajax-review-cards'),
    
    path('api/',  views.api_view, name='api'),
    
]
