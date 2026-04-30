from django import forms

from apps.projects.models import ProjectCategory, Project


class ProjectCategoryForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des catégories de projets.
    """
    class Meta:
        model = ProjectCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Development Applicatifs, Data Science, etc.'
            }),
        }

        labels = {
            'name': 'Nom de la catégorie'
        }


class ProjectForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des projets.
    """
    class Meta:
        model = Project
        fields = ['title', 'category', 'start_date',  'end_date', 'source_code_url', 'image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Ex: Development Applicatifs, Data Science, etc.'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Ex: Development Applicatifs, Data Science, etc.'
            }),
            'category': forms.Select(attrs={
                'placeholder': 'Ex: Development Applicatifs, Data Science, etc.'
            }),
            'technologies': forms.SelectMultiple(attrs={
                'placeholder': 'Ex: Development Applicatifs, Data Science, etc.'
            }),
            'url': forms.URLInput(attrs={
                'placeholder': 'Ex: https://www.google.com'
            }),
            'image': forms.FileInput(attrs={
                'placeholder': 'Ex: https://www.google.com'
            }),
        }

        labels = {
            'title': 'Titre du projet',
            'description': 'Description du projet',
            'category': 'Catégorie du projet',
            'technologies': 'Technologies utilisées',
            'url': 'URL du projet',
            'image': 'Image du projet'
        }