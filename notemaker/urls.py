from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('fake/', views.FakeWebsiteView.as_view(), name='fake_website'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note-details'),
    path('card/<int:pk>/', views.card_detail_view, name='card-details'),
    
    path('ajax/testing/', views.test_ajax, name='test_ajax'),
    path('ajax/anki_generate_note/', views.ajax_anki_generate_note, name='ajax_anki_generate_note'),
    path('ajax/anki_create_note/', views.ajax_anki_create_note, name='ajax_anki_create_note'),
    
]
