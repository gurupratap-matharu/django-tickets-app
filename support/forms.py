from django import forms
from .models import Ticket

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['vendor', 'category', 'severity', 'description']


