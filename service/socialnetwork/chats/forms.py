from django import forms
from .models import Message, ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageCreateForm(forms.ModelForm):
    """Form for creating a new message."""
    class Meta:
        model = Message
        fields = ("body",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # changing field's params
        self.fields["body"].widget.attrs.update({"placeholder": "Введите сообщение..."})
        self.fields["body"].label = ""


class PersonalChatRoomCreateForm(forms.ModelForm):
    """
    Form for creating a new personal chat room.
    Don't dedicated for displaying on page (just validating data).
    Should be prepopulated with members in a view.
    """
    class Meta:
        model = ChatRoom
        fields = ("members",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["members"].widget = forms.MultipleHiddenInput()

    def clean_members(self):
        if len(self.cleaned_data["members"]) != 2:
            raise forms.ValidationError(
                "В персональном чате должно быть не более двух участников."
            )
        return self.cleaned_data["members"]


class GroupChatRoomCreateForm(forms.ModelForm):
    """
    Form for creating a new group.
    Takes members queryset as an argument to pass in available users to choose from for adding to group.
    Current user also adding to members in a view after processing form.
    """
    class Meta:
        model = ChatRoom
        fields = ("name", "members")

    def __init__(self, *args, **kwargs):
        members_queryset = kwargs.pop("members_queryset", None)
        super().__init__(*args, **kwargs)
        # specifying queryset of members to choose from (gonna be curr user's friends, followers etc.)
        self.fields["members"].queryset = members_queryset or User.objects.all()

    def clean_members(self):
        # on this step in members aren't curr user which will be added later
        if len(self.cleaned_data["members"]) < 2:
            raise forms.ValidationError(
                "В групповом чате должно быть не менее трех участников (включая владельца)."
            )
        return self.cleaned_data["members"]
