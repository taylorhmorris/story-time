from django.http import HttpResponse
from django.views import generic

from .models import Story, Translation

class IndexView(generic.ListView):
    template_name = 'storytime/index.html'
    context_object_name = 'stories'
    
    def get_queryset(self):
        return {}
    
    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['stories'] = Translation.objects.all()
        if 'lang' in self.kwargs:
            context['lang'] = self.kwargs['lang']
        else:
            context['lang'] = "English"
        return context
    
class StoryView(generic.DetailView):
    model = Story
    template_name = 'storytime/index.html'
