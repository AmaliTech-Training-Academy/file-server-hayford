from django.db import models
from django.urls import reverse

# Create your models here.
class FileModels(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(models.FileField(upload_to='files'))
    downloads = models.IntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
    thumbnail = models.FileField(upload_to='thumbnail/', null=True, blank=True)
                            


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
      return reverse('filesystem:file_list', kwargs={'pk': self.pk, 'slug': self.slug })
    
class FileSearch(models.Model):
   name = models.CharField(max_length=200)

   def search(self, query):
      return FileModels.objects.filter(title_icontains=query)