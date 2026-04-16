from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.education.models import EducationSection, Education


class EducationSectionForm(forms.ModelForm):
    """
    Form for creating and updating an EducationSection instance.

    This form allows users to define an academic section title
    and an optional rich-text description.
    """

    class Meta:
        """
        Meta configuration for EducationSectionForm.
        """

        model = EducationSection

        fields = (
            "name",
            "description",
        )

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ex: Parcours Académique"}),
            "description": CKEditor5Widget(config_name="extends", attrs={"placeholder": "Description introductive du parcours académique (optionnelle)."}),
        }

        labels = {
            "name": "Titre de la section",
            "description": "Description",
        }

        help_texts = {
            "name": "Titre de la section (ex: Parcours Académique).",
            "description": "Description introductive du parcours académique (optionnelle).",
        }






class EducationForm(forms.ModelForm):
    """
    Form for creating and updating an Education instance.

    This form allows users to define academic background information
    including school, degree, field of study and dates.
    """

    class Meta:
        """
        Meta configuration for EducationForm.
        """

        model = Education

        fields = (
            "school",
            "degree",
            "field_of_study",
            "start_date",
            "end_date",
            "description",
        )

        widgets = {
            "school": forms.TextInput(attrs={"placeholder": "Université Le Havre Normandie"}),
            "degree": forms.TextInput(attrs={"placeholder": "Master 2"}),
            "field_of_study": forms.TextInput(attrs={"placeholder": "Mathématiques Appliquées"}),
            "description": CKEditor5Widget(config_name="default", attrs={"placeholder": "Description optionnelle (résultats, projets, mentions...)"}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

        labels = {
            "school": "Établissement",
            "degree": "Diplôme",
            "field_of_study": "Domaine d'étude",
            "start_date": "Date de début",
            "end_date": "Date de fin",
            "description": "Description",
        }

        help_texts = {
            "end_date": "Laisser vide si la formation est en cours.",
            "field_of_study": "Optionnel (ex: Informatique, Mathématiques).",
            "description": "Description optionnelle (résultats, projets, mentions...).",
        }