from django import forms

from apps.certifications.models import Certification


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuer', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: AWS Certified Solutions Architect'}),
            'issuer': forms.TextInput(attrs={
                'placeholder': 'Ex: Amazon Web Services, Coursera, etc.'}),
            'order': forms.NumberInput(attrs={
                'min': 0
            }),
        }

    label = {
        'name': 'Nom de la certification',
        'issuer': 'Organisme délivrant la certification',
        'order': 'Ordre d\'affichage',
    }
