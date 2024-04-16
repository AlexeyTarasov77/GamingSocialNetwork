from django import forms
from django.core.validators import RegexValidator

class CouponApplyForm(forms.Form):
    code = forms.CharField(label='Код купона', validators=[RegexValidator(r'^[a-zA-Z0-9]*$')])