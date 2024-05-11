from django import forms
from .models import Team, Ad


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "description", "logo", "game"]
        
        
class AdCreateForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ["title", "description", "game", "photo", "type"]
        
    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data["type"]
        profile = cleaned_data["user"].profile
        if type == Ad.TYPE_CHOICES["RECRUITING"] and not profile.is_leader: 
            raise forms.ValidationError("Для создания рекрутингового объявления необходимо быть лидером команды, но вы им не являетесь.")