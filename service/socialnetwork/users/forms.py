from django import forms
from .models import Profile
from django.contrib.auth import get_user_model

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=50, required=False, label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'form-control'})) # поле для изменения username для связанного юзера
    email = forms.EmailField(label="Электронная почта", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ['image', 'bg_image', 'bio', 'date_of_birth']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'bg_image': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'date_of_birth': forms.SelectDateWidget(attrs={'class': 'form-control'}, years=range(1980, 2025))
        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.order_fields(['username', 'email', 'bio', 'image', 'bg_image', 'date_of_birth'])
            self.fields['username'].initial = self.instance.user.username  
            self.fields['email'].initial = self.instance.user.email

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exclude(pk=self.instance.user.pk).exists(): # проверка на уникальность 
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def save(self, commit=True): # при сохранении обновить у пользователя username взятый с формы
        user = self.instance.user 
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()
        return super().save(commit)
        

        