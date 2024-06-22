from django import forms
from .models import Message, ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'placeholder': 'Введите сообщение...'})
        self.fields['body'].label = ''


class PersonalChatRoomCreateForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ('members',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].widget = forms.MultipleHiddenInput()

    def clean_members(self):
        if len(self.cleaned_data['members']) != 2:
            raise forms.ValidationError('В персональном чате должно быть не более двух участников.')
        return self.cleaned_data['members']


class GroupChatRoomCreateForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ('name', 'members')

    def __init__(self, *args, **kwargs):
        members_queryset = kwargs.pop('members_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = members_queryset or User.objects.all()

    def clean_members(self):
        if len(self.cleaned_data['members']) < 3:
            raise forms.ValidationError('В групповом чате должно быть не менее трех участников.')
        return self.cleaned_data['members']
