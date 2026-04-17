from django import forms
from .models import TechStackCategory, TechStack


class TechStackCategoryForm(forms.ModelForm):
    class Meta:
        model = TechStackCategory
        fields = ["name", "order"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Ex: Backend, Data, DevOps..."
            }),
            "order": forms.NumberInput(attrs={
                "min": 0
            }),
        }


class TechStackForm(forms.ModelForm):
    class Meta:
        model = TechStack
        fields = ["category", "name"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Ex: Python, Django, SQL..."
            }),
        }

    label = {
        "category": "Catégorie",
        "name": "Nom",
    }
