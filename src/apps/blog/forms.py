from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.blog.models import PostCategory, PostTag, Post


class PostCategoryForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des catégories des articles.
    """

    class Meta:
        model = PostCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ex: CI/CD avec GitHub Actions"}
            ),
        }

        labels = {"name": "Nom catégorie articles"}


class PostTagForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des tags des articles.
    """

    class Meta:
        model = PostTag
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ex: DevOps, Data, etc."}
            ),
        }

        labels = {"name": "Nom du tag"}


class PostForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des articles.
    """

    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "published_at",
            "image",
            "tags",
            "is_active",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Ex: Development Applicatifs, Data Science, etc."}
            ),
            "category": forms.Select(
                attrs={"placeholder": "Ex: Development Applicatifs, Data Science, etc."}
            ),
            "published_at": forms.DateInput(attrs={"type": "date"}),
            "image": forms.FileInput(),
            "tags": forms.SelectMultiple(attrs={"class": "chosen-select"}),
            "is_active": forms.CheckboxInput(),
            "description": CKEditor5Widget(
                config_name="extends",
                attrs={"placeholder": "Ex: CI/CD avec github actions, les bonne pratiques..."},
            ),
        }

        labels = {
            "title": "Titre du l'article",
            "category": "Catégorie de l'article",
            "published_at": "Date de début de publication",
            "image": "Image du l'article",
            "tags": "Tags de l'article'",
            "is_active": "Article actif ?",
            "description": "Description de l'article",
        }
