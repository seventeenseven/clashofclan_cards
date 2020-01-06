from django import forms
from .models import Cards


class CardForm(forms.ModelForm):

    class Meta:
        model = Cards
        fields = ['name','village', 'level', 'maxLevel', 'heroes', 'xp', 'type', 'card_images']
