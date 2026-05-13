from django import forms

from apps.certifications.models import Certification


class CertificationForm(forms.ModelForm):
    """
    Form for creating and updating certifications.
    """

    class Meta:
        model = Certification
        fields = [
            "name",
            "issuer",
            "certificate_url",
            "image",
            "obtained_date",
            "order",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ex: AWS Certified Solutions Architect"}
            ),
            "issuer": forms.TextInput(
                attrs={"placeholder": "Ex: Amazon Web Services, Coursera, etc."}
            ),
            "certificate_url": forms.URLInput(
                attrs={
                    "placeholder": "Ex: https://www.coursera.org/account/accomplishments/verify/ABC123"
                }
            ),
            "image": forms.FileInput(attrs={"accept": "image/*"}),
            "obtained_date": forms.DateInput(attrs={"type": "date"}),
            "order": forms.NumberInput(attrs={"min": 0}),
        }

    label = {
        "name": "Nom de la certification",
        "issuer": "Organisme délivrant la certification ou lien",
        "certificate_url": "Lien du certificat",
        "image": "Image du certificat",
        "obtained_date": "Date d'obtention",
        "order": "Ordre d'affichage",
    }
