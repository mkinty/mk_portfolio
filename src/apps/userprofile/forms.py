from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.userprofile.models import UserProfile


class UserProfileForm(ModelForm):
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
        fields = ['title', 'position', 'avatar', 'bio']
        widgets = {
            "bio": CKEditor5Widget(config_name="default"),
        }