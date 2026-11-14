from django import forms
from .models import ValentinePlan


class PlannerForm(forms.ModelForm):
    """Form for creating Valentine plans"""
    
    class Meta:
        model = ValentinePlan
        fields = ['your_name', 'partner_name', 'relationship_type', 'city', 'budget', 'plan_type', 'vibe', 'about_partner', 'about_yourself', 'special_request']
        
        widgets = {
            'your_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Your Name',
                'required': True,
            }),
            'partner_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Their Name',
            }),
            'relationship_type': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': True,
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. Bhubaneswar, Delhi',
                'required': True,
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. 2000',
                'min': 100,
                'required': True,
            }),
            'plan_type': forms.HiddenInput(),
            'vibe': forms.HiddenInput(),
            'about_partner': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Their interests, hobbies, favorite things...',
                'rows': 3,
            }),
            'about_yourself': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your relationship story, what makes you special together...',
                'rows': 3,
            }),
            'special_request': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any specific ideas or preferences?',
                'rows': 2,
            }),
        }
        
        labels = {
            'your_name': '🙋 Your Name',
            'partner_name': '💝 Their Name',
            'relationship_type': '❤️ Relationship Type',
            'city': '📍 City / Location',
            'budget': '💰 Budget (₹)',
            'plan_type': '📅 Pick Your Date',
            'vibe': '✨ Vibe',
            'about_partner': '💝 Tell us about them',
            'about_yourself': '💭 Tell us about you two',
            'special_request': '💡 Suggest something special',
        }

    def clean_partner_name(self):
        """Make partner_name optional for self-love plans"""
        relationship_type = self.cleaned_data.get('relationship_type')
        partner_name = self.cleaned_data.get('partner_name')
        
        if relationship_type == 'self_love':
            return partner_name or 'Me'
        
        if not partner_name or partner_name.strip() == '':
            raise forms.ValidationError('Please enter their name.')
        
        return partner_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make partner_name not required at field level (validated in clean)
        self.fields['partner_name'].required = False


class ReactionForm(forms.Form):
    """Form for adding reactions to shared plans"""
    
    REACTION_CHOICES = [
        ('loved', '❤️ Loved it'),
        ('shocked', '😳 Shocked'),
        ('emotional', '🥹 Emotional'),
        ('laughing', '😂 Laughing'),
        ('crying', '😭 Crying'),
    ]
    
    reaction_type = forms.ChoiceField(
        choices=REACTION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=True
    )
