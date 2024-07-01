from django import forms
from django.utils.translation import gettext as _
from taggit.models import Tag

from .models import Comment, Post


class ShareForm(forms.Form):
    to = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "yourgmail@gmail.com"}
        ),
        label=_("Email адресс получателя"),
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        label=_("Заметки"),
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
                "placeholder": _("Введите комментарий"),
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["content"]


class CreatePostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ["title", "content", "status", "photo", "tags"]
        help_texts = {
            "title": _("Введите имя поста"),
            "content": _("Введите текст поста"),
            "status": _("Установите статус поста"),
            "tags": _("Выберите подходящие теги для вашего поста"),
        }
        labels = {
            "title": _("Заголовок поста"),
            "content": _("Текст поста"),
            "status": _("Статус поста"),
            "photo": _("Фото поста *опционально"),
            "tags": _("Теги"),
        }
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5, "columns": "10"}),
        }


class UpdatePostForm(CreatePostForm):
    pass
