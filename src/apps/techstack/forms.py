from django import forms

from apps.techstack.models import TechStackCategory, TechStack


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

        labels = {
            "name": "Nom",
            "order": "Ordre",
        }


class TechStackForm(forms.ModelForm):
    class Meta:
        model = TechStack
        fields = ["category", "name"]
        widgets = {
            "category": forms.Select(attrs={
                "placeholder": "Sélectionnez une catégorie"
            }),
            "name": forms.TextInput(attrs={
                "placeholder": "Ex: Python, Django, SQL..."
            }),
        }

    label = {
        "category": "Catégorie",
        "name": "Nom",
    }
