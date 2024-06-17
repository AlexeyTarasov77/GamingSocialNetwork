from django import forms
from .models import Message, Chat

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)


class ChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('name', 'participants')
        
    def __init__(self, *args, **kwargs):
        self.fields['participants'].required = False
        
        
    