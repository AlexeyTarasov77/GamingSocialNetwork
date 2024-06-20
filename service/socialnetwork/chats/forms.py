from django import forms
from .models import Message, ChatRoom

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'rows': 3, 'placeholder': 'Введите сообщение...'})
        self.fields['body'].label = ''


class ChatCreateForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ('name', 'members')
        
    def __init__(self, *args, **kwargs):
        self.fields['members'].required = False
        
        
    