from datetime import timezone
from django import forms
from .models import BaseInfo, InventoryItem
from django.forms.widgets import DateInput
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})



class BaseInfoForm(forms.ModelForm):
    class Meta:
        model = BaseInfo
        fields = '__all__'
        



class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        
        widgets = {
            'start_date': DateInput(
                attrs={'type': 'date', 'class': 'form-select ',
            },
                format='%dd-%m-%Y',
                
            ),
        }
        
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if 'date_field' in self.fields:
                    self.fields['date_field'].input_formats = ['%d-%m-%Y'] 
    
