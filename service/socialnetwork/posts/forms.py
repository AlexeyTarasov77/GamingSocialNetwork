from collections.abc import Mapping
from typing import Any

from django import forms
from taggit.models import Tag
from .models import Comment, Post


class ShareForm(forms.Form):
    to = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "yourgmail@gmail.com"}
        ),
        label="Email адресс получателя",
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        label="Заметки",
        required=False,
    )


class CommentForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "cols": 25,
                "placeholder": "Введите комментарий",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["content"]


class CreatePostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = Post
        fields = ["name", "content", "status", "photo", "tags"]
        help_texts = {
            "name": "Введите имя поста",
            "content": "Введите текст поста",
            "status": "Установите статус поста",
            "tags": "Выберите подходящие теги для вашего поста",
        }
        labels = {
            "name": "Заголовок поста",
            "content": "Текст поста",
            "status": "Статус поста",
            "photo": "Фото поста *опционально",
            "tags": "Теги",
        }
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5, "columns": "10"}),
        }


class UpdatePostForm(CreatePostForm):
    pass
