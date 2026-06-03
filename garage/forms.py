from django import forms
from .models import Car, CarModel


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'vin', 'color', 'license_plate', 'engine_volume', 'horsepower', 'transmission', 'drive', 'photo']
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '17'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'engine_volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'horsepower': forms.NumberInput(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'drive': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].widget.attrs.update({'class': 'form-select'})
        self.fields['brand'].label = 'Марка'
        
        self.fields['model'].widget.attrs.update({'class': 'form-select'})
        self.fields['model'].label = 'Модель'
        self.fields['model'].queryset = CarModel.objects.none()
        
        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = CarModel.objects.filter(brand_id=brand_id)
            except (ValueError, TypeError):
                pass
        
        self.fields['year'].label = 'Год выпуска'
        self.fields['vin'].label = 'VIN номер'
        self.fields['color'].label = 'Цвет'
        self.fields['license_plate'].label = 'Госномер'
        self.fields['engine_volume'].label = 'Объём двигателя (л)'
        self.fields['horsepower'].label = 'Мощность (л.с.)'
        self.fields['transmission'].label = 'Коробка передач'
        self.fields['drive'].label = 'Привод'
        self.fields['photo'].label = 'Фото автомобиля'
    
    def clean(self):
        cleaned_data = super().clean()
        brand = cleaned_data.get('brand')
        model = cleaned_data.get('model')
        
        if brand and model and model.brand != brand:
            self.add_error('model', 'Выберите модель, соответствующую марке')
        
        return cleaned_data