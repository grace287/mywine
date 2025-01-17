from django import forms
from .models import TastingNote

class TastingNoteForm(forms.ModelForm):
    class Meta:
        model = TastingNote
        fields = [
            'wine_name', 'wine_type', 'winery', 'vintage',
            'country', 'grape_varieties', 'tasting_date',
            'tasting_place', 'appearance_intensity',
            'appearance_clarity', 'aroma_notes',
            'taste_sweetness', 'taste_acidity',
            'taste_tannin', 'taste_body',
            'taste_notes', 'rating', 'overall'
        ]
        widgets = {
            'tasting_date': forms.DateInput(attrs={'type': 'date'}),
            'appearance_intensity': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5'}),
            'aroma_intensity': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5'}),
            'taste_sweetness': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5'}),
            'taste_acidity': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5'}),
            'taste_tannin': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5'}),
            'taste_body': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5'}),
            'rating': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 필수가 아닌 필드 설정
        optional_fields = [
            'winery', 'vintage', 'country', 'grape_varieties',
            'tasting_place', 'appearance_intensity',
            'appearance_clarity', 'aroma_notes',
            'taste_sweetness', 'taste_acidity',
            'taste_tannin', 'taste_body',
            'taste_notes', 'overall'
        ]
        
        for field in optional_fields:
            self.fields[field].required = False