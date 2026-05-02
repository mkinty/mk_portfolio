from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.project.models import ProjectCategory, Project, Tag


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


class TagForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des tags.
    """

    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Development, Data, etc.'
            }),
        }

        labels = {
            'name': 'Nom du tag'
        }


class ProjectForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des projets.
    """

    class Meta:
        model = Project
        fields = ['title', 'category', 'start_date', 'end_date', 'source_code_url', 'image', 'tags', 'is_active',
                  'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Ex: Development Applicatifs, Data Science, etc.'
            }),
            'category': forms.Select(attrs={
                'placeholder': 'Ex: Development Applicatifs, Data Science, etc.'
            }),
            'start_date': forms.DateInput(attrs={"type": "date"}),
            'end_date': forms.DateInput(attrs={"type": "date"}),
            'source_code_url': forms.URLInput(attrs={
                'placeholder': 'Ex: https://www.google.com'
            }),
            'image': forms.FileInput(),
            'tags': forms.SelectMultiple(attrs={
                'class': 'chosen-select'
            }),
            'is_active': forms.CheckboxInput(),
            'description': CKEditor5Widget(config_name="extends", attrs={
                'placeholder': 'Ex: Development de l\'application...'
            }),
        }

        labels = {
            'title': 'Titre du projet',
            'category': 'Catégorie du projet',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'source_code_url': 'URL du code source',
            'image': 'Image du projet',
            'tags': 'Tags',
            'is_active': 'Projet actif',
            'description': 'Description du projet'
        }
