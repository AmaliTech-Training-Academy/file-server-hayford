from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FileForm, SendFileForm
from authentication_app.models import CustomUser
from .thumbnails import generate_thumbnail
from django.core.files.base import ContentFile
from django.http import HttpResponseForbidden, FileResponse
from .models import FileModels
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils. decorators import method_decorator
from django.views.generic import ListView, DetailView

# Create your views here.
# def upload(request):
#     if request.method == 'POST':
#         file = request.FILES['files']
#         # print(file.name)
#         storage = FileSystemStorage()
#         storage.save(file.name, file)
#     return render(request, 'filesystem/upload.html')

# def upload_book(request):
#     if request.method == 'POST':
#         form=BookForm
#     return render(request, 'filesystem/upload_book.html')


# def book_list(request):
#     return render(request, 'filesystem/book_list.html')


# @login_required
def upload_file(request):
    user= CustomUser.objects.get(pk=request.user.pk)
    if user.is_superuser:
        if request.method =="POST":
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.save()
                if file.file.name.lower().endswith('.pdf'):
                    file = form.save()
                    file.user = request.user
                    file_path = file.file.path
                    thumbnail = generate_thumbnail(file_path)

                    file.thumbnail.save(f'{file.title}_thumbnail.jpg', ContentFile(thumbnail))
                else:
                    form.save()
                return redirect('filesystem:upload_list')
        else:
            form = FileForm()
        return render(request, 'filesystem/upload_file.html', {'form': form}) 
    else:
        return HttpResponseForbidden('<h1>You are not authorised to view this page</h1>')



@login_required
def download_file(request, file_id):
    file = FileModels.objects.get(pk=file_id)
    response = FileResponse(file.file, as_attachment=True)
    file.downloads += 1
    file.save()
    return response



@login_required
def send_file_email(request, file_id):
    file = get_object_or_404(FileModels, pk=file_id)
    if request.method == 'POST':
        form = SendFileForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email= EmailMessage(
                subject, 
                message, 
                settings.EMAIL_HOST_USER, 
                [recipient_email], 
                reply_to=['another@example.com']
                )
            email.attach_file(file.file.path)
            email.send()
            file.emails_sent += 1
            file.save()
            return redirect('filesystem:upload_list')
        else:
            form = SendFileForm()
        return render(request, 'filesystem/send_file.html', {'form': form, 'file': file})
    


@method_decorator(login_required, name='dispatch')
class FileListView(ListView):
    model = FileModels
    template_name = 'filesystem/upload_list.html'
    context_object_name = 'files'
    ordering = ['title']
    paginate_by = 20



@method_decorator(login_required, name='dispatch')
class FileDetailView(DetailView):
    model = FileModels
    template_name = 'filesystem/file_detail.html'

    def get_context_data(self, **kwargs):
        parameter= super().get_context_data(**kwargs)
        parameter['file'] = self.get_object()
        return parameter
    


@login_required
def log(request):
    user = CustomUser.objects.get(request.user.pk)
    if user.is_superuser:
        files = FileModels.objects.all()
        return render(request, 'filesystem/logs.html', {'files': files})
    else:
        return HttpResponseForbidden('<h1>You are not authorised to view thsi page</h1>')
    


@login_required
def search_view(request):
    query = request.GET.get('q')
    if query:
        files = FileModels.objects.filter(title_icontains = query)
    else:
        files = []
    return render(request, 'filesystem/search.html', {'files': files})



@login_required
def preview(request, file_id):
    file = get_object_or_404(FileModels, id=file_id)
    if file.file.name.lower().endswith():
        return FileResponse(open(file,file.path, 'rb'), content_type='application/pdf')
    else:
        return render(request, 'filesystem/preview.html', {'file': file})
    


@login_required
def open_page(request, file_id):
    file = get_object_or_404(FileModels, id=file_id)
    return render(request, 'filesystem/open_page.html', {'file': file})