from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files. storage import FileSystemStorage
from .forms import BookForm

# Create your views here.
class home(TemplateView):
    template_name='filesystem/home.html'

def upload(request):
    if request.method == 'POST':
        file = request.FILES['files']
        # print(file.name)
        storage = FileSystemStorage()
        storage.save(file.name, file)
    return render(request, 'filesystem/upload.html')

def upload_book(request):
    if request.method == 'POST':
        form=BookForm
    return render(request, 'filesystem/upload_book.html')


def book_list(request):
    return render(request, 'filesystem/book_list.html')