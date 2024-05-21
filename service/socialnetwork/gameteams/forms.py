from django import forms
from .models import Team, Ad


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "description", "logo", "game", "country"]
        
        
class AdCreateForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ["title", "content", "game", "photo", "type"]
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.user = user
        
    def clean(self):
        cd = super().clean()
        print(cd)
        type = cd["type"]
        profile = self.user.profile
        if type == "RECRUITING" and not profile.is_team_leader: 
            raise forms.ValidationError("Для создания рекрутингового объявления необходимо быть лидером команды, но вы им не являетесь.")