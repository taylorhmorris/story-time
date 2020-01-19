from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.
class Story(models.Model):
    original_source_title = models.CharField(max_length=200)
    original_source_author = models.CharField(max_length=200)
    adaptation_author = models.CharField(max_length=200)
    
    def __str__(self):
        return "{} by {}".format(self.original_source_title, self.original_source_author)
    
class Language(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Translation(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, null=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    main_text = models.TextField()
    author = models.CharField(max_length=200)
    slug = models.SlugField(default='', editable=False, max_length=200)
    
    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('story-pk-slug', kwargs=kwargs)
    
    def save(self, *args, **kwargs):
        value = self.title
        if not self.id:
            self.slug = slugify(f"{self.title}-{self.story.original_source_author}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "{} by {}".format(self.title, self.author)
