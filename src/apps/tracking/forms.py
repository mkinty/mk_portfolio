from django import forms

from apps.tracking.models import (
    JobApplication,
    ApplicationFollowUp,
)


class JobApplicationForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des candidatures.
    """

    class Meta:
        model = JobApplication
        fields = [
            'position',
            'company',
            'job_offer_link',
            'job_offer_file',
            'resume',
            'cover_letter',
            'application_date',
            'application_status',
        ]

        widgets = {
            'position': forms.TextInput(attrs={
                'placeholder': 'Ex: Développeur Backend Django'
            }),

            'company': forms.TextInput(attrs={
                'placeholder': 'Ex: OpenAI'
            }),

            'job_offer_link': forms.URLInput(attrs={
                'placeholder': 'Ex: https://www.example.com/job-offer'
            }),

            'job_offer_file': forms.FileInput(),

            'resume': forms.FileInput(),

            'cover_letter': forms.FileInput(),

            'application_date': forms.DateInput(attrs={
                'type': 'date'
            }),

            'application_status': forms.Select(),
        }

        labels = {
            'position': 'Poste',
            'company': 'Entreprise',
            'job_offer_link': 'Lien de l’offre',
            'job_offer_file': 'Fichier de l’offre',
            'resume': 'CV',
            'cover_letter': 'Lettre de motivation',
            'application_date': 'Date de candidature',
            'application_status': 'État de la candidature',
        }


class ApplicationStatusForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des candidatures.
    """

    class Meta:
        model = JobApplication
        fields = [
            'application_status',
        ]

        widgets = {
            'application_status': forms.Select(),
        }

        labels = {
            'application_status': 'État de la candidature',
        }


class ApplicationFollowUpForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification des éléments de suivi.
    """

    class Meta:
        model = ApplicationFollowUp

        fields = [
            'title',
            'event_date',
            'status',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Ex: Premier entretien RH'
            }),

            'event_date': forms.DateInput(attrs={
                'type': 'date'
            }),

            'status': forms.Select(),
        }

        labels = {
            'title': 'Intitulé',
            'event_date': 'Date',
            'status': 'Statut',
        }
