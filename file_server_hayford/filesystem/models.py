from django.db import models
from django.urls import reverse

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    file = models.FileField(upload_to='books/pdfs/')
    is_published = models.DateField(default=True)

    # is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
      return reverse('filesystem:file_list', kwargs={'pk': self.pk, 'slug': self.slug })