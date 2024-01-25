from django import forms

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
    

    
