from django import forms

from apps.techstack.models import TechStackCategory, TechStack


class TechStackCategoryForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des catégories de tech stack.
    """
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
            "order": "Ordre d'affichage",
        }


class TechStackForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des tech stacks.
    """
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
