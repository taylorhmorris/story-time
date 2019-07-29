from django.urls import path

from . import views

urlpatterns = [
    path('<str:lang>/', views.IndexView.as_view(), name='index'),
    path('<str:lang>/<int:pk>/', views.StoryView.as_view(), name='story'),
    path('', views.IndexView.as_view(), name='index_default'),
]

