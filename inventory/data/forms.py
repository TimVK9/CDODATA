from django import forms
from .models import *
from django.forms import TextInput




class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        
        widgets = {
            'start_data': TextInput(attrs={
                'type': 'date',
                'placeholder': 'Выберите дату'
            }),
            'name': TextInput(attrs={
                'placeholder': 'Введите название'
            }),
            'description': TextInput(attrs={
                'placeholder': 'Введите подробное описание объекта'
            })
        }



class UploadFileForm(forms.Form):
    file = forms.FileField()
