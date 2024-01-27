from django import forms
from .models import Comment

class ShareForm(forms.Form):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'display:none'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'style': 'display:none'}))
    to = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'yourgmail@gmail.com'}),
        label='Email адресс получателя',
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
        label='Заметки',
    )
    

class CommentForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    content = forms.CharField(label = '', widget=forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'cols':25, 'placeholder':'Введите комментарий'}))
    class Meta:
        model = Comment
        fields = ['content']