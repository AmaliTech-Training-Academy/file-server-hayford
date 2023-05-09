from django import forms
from .models import FileModels

class FileForm(forms.ModelForm):
    class Meta:
        model=FileModels
        fields=('title', 'description', 'file')


class SendFileForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient Email')
    subject = forms. CharField(label='Subject')
    message = forms.CharField(widget=forms.Textarea, label='Message')