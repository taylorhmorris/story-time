from django.urls import path

from . import views

app_name = 'storytime'
urlpatterns = [
    path('<str:lang>/', views.IndexView.as_view(), name='index'),
    path('<str:lang>/<int:pk>/', views.StoryView.as_view(), name='story'),
    path('<str:lang>/<slug:slug>/', views.StoryView.as_view(), name='story_slug'),    
    path('', views.IndexView.as_view(), name='index_default'),
]

