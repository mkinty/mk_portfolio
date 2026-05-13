from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.skills.models import Skills


class SkillsForm(forms.ModelForm):
    """
    Form for creating and updating a Skills instance.

    This form allows users to define a skill name and an optional
    rich-text description using CKEditor 5.
    """

    class Meta:
        """
        Meta configuration for SkillsForm.

        Attributes:
            model (Skills): Model associated with this form.
            fields (tuple): Fields included in the form.
            widgets (dict): Custom widgets used in the form.
            labels (dict): Human-readable field labels.
        """

        model = Skills

        fields = (
            "name",
            "description",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ex: Compétences Techniques"}
            ),
            "description": CKEditor5Widget(
                config_name="extends",
                attrs={
                    "placeholder": "Description de la catégorie "
                    "de compétences (optionnelle)."
                },
            ),
        }

        labels = {
            "name": "Nom de la catégorie de compétences",
            "description": "Description",
        }
