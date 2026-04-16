from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.userprofile.models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form for creating and updating a UserProfile instance.

    This form uses CKEditor 5 for the `bio` field to provide
    a rich text editing experience.

    Fields:
        title (str): User title.
        position (str): User position.
        avatar (Image/File): Profile avatar image.
        bio (str): User biography (rich text via CKEditor 5).

    Notes:
        - The `bio` field uses CKEditor5Widget with the "default" configuration.
        - Other fields use Django default widgets.
        - This form can be reused for both create and update views.
    """

    class Meta:
        """
        Meta configuration for UserProfileForm.

        Attributes:
            model (UserProfile): Model associated with this form.
            fields (list[str]): Fields included in the form.
            widgets (dict): Custom widgets for specific fields.
        """

        model = UserProfile
        fields = (
            "title",
            "position",
            "birth_date",
            "location",
            "phone",
            "avatar",
            "bio"
        )

        widgets = {
            "bio": CKEditor5Widget(config_name="extends"),
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

        labels = {
            "title": "Titre professionnel",
            "position": "Poste actuel",
            "birth_date": "Date de naissance",
            "location": "Lieu de localisation",
            "phone": "Numéro de téléphone",
            "avatar": "Photo de profil",
            "bio": "Biographie",
        }

        help_texts = {
            "title": "Ex : Développeur Full Stack",
        }
