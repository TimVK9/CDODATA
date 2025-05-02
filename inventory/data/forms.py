from datetime import timezone
from django import forms
from .models import BaseInfo, InventoryItem
from django.forms.widgets import DateInput

class BaseInfoForm(forms.ModelForm):
    class Meta:
        model = BaseInfo
        fields = '__all__'
        



class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        
        widgets = {
            'date_field': DateInput(
                attrs={'type': 'date', 'class': 'form-control form-control-sm',
            },
                format='%d-%m-%Y',
                
            ),
        }
        
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if 'date_field' in self.fields:
                    self.fields['date_field'].input_formats = ['%d-%m-%Y'] 
    
