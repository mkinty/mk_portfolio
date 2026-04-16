from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.experiences.models import Experience


class ExperienceForm(forms.ModelForm):
    """
    Form for creating and updating an Experience instance.

    This form uses CKEditor 5 for the description field to provide
    a rich text editing experience and HTML5 date inputs for dates.
    """

    class Meta:
        """
        Meta configuration for ExperienceForm.

        Attributes:
            model (Experience): Model associated with this form.
            fields (tuple): Fields included in the form.
            widgets (dict): Custom widgets for specific fields.
        """

        model = Experience
        fields = (
            "title",
            "company",
            "location",
            "start_date",
            "end_date",
            "is_current",
            "description",
        )

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Ex: Développeur Full-Stack"}),
            "company": forms.TextInput(attrs={"placeholder": "Ex: Tech Solutions Inc."}),
            "location": forms.TextInput(attrs={"placeholder": "Ex: Paris, France"}),
            "description": CKEditor5Widget(config_name="extends", attrs={"placeholder": "Description détaillée des responsabilités et réalisations (optionnelle)."}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "is_current": forms.CheckboxInput(),
        }

        labels = {
            "title": "Intitulé du poste",
            "company": "Entreprise",
            "location": "Lieu de localisation",
            "start_date": "Date de début",
            "end_date": "Date de fin",
            "is_current": "Poste actuel",
            "description": "Description",
        }

        help_texts = {
            "end_date": "Leave empty if this is your current position.",
        }
