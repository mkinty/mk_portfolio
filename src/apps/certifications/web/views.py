from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.certifications.selectors.certifications_selectors import (
    CertificationsSelectors,
)
from apps.certifications.services.certifications_services import CertificationsServices
from apps.users.selectors.user_selectors import get_user_by_id


class CertificationsAddView(View):
    """
    Create a new certification
    - GET: Display the form to add a new certification
    - POST: Handle the form submission to add a new certification
    """

    template_name = "certifications/form.html"
    title = "Ajouter une certification"

    def get(self, request, user_id):
        """Display the creation form"""
        form, user_obj = CertificationsServices.get_add_certification_form(user_id)
        return render(
            request,
            self.template_name,
            {"form": form, "user_obj": user_obj, "title": self.title},
        )

    def post(self, request, user_id):
        """Handle form submission"""
        user_obj = get_user_by_id(user_id)
        success, form, certification = CertificationsServices.create_certification(
            user_obj, request.POST, request.FILES
        )
        if not success:
            messages.error(
                request,
                "Erreur lors de l'ajout de la certification ! "
                "Veuillez vérifier les champs du formulaire.",
            )
            return render(
                request,
                self.template_name,
                {"form": form, "user_obj": user_obj, "title": self.title},
            )
        messages.success(request, "Certification ajoutée avec succès!")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class CertificationsUpdateView(View):
    """
    Update an existing certification
    - GET: Display the form to update an existing certification
    - POST: Handle the form submission to update an existing certification
    """

    template_name = "certifications/form.html"
    title = "Modifier une certification"

    def get(self, request, certification_id):
        """Display the update form"""
        form, certification = CertificationsServices.get_update_certification_form(
            certification_id
        )
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "certification": certification,
                "user_obj": certification.user,
                "title": self.title,
            },
        )

    def post(self, request, certification_id):
        """Handle form submission"""
        success, form, certification = CertificationsServices.update_certification(
            certification_id, request.POST, request.FILES
        )
        if not success:
            messages.error(
                request,
                "Erreur lors de la mise à jour de la certification ! "
                "Veuillez vérifier les champs du formulaire.",
            )
            return render(
                request,
                self.template_name,
                {"form": form, "certification": certification, "title": self.title},
            )
        messages.success(request, "Certification mise à jour avec succès!")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class CertificationsDeleteView(View):
    """
    Delete a certification
    - GET: Display a confirmation dialog
    - POST: Handle the form submission to delete a certification
    """

    template_name = "certifications/delete_confirm.html"
    title = "Supprimer une certification"

    def get(self, request, certification_id):
        """Display a confirmation dialog"""
        certification = CertificationsSelectors.get_certification_by_id(
            certification_id
        )
        return render(
            request,
            self.template_name,
            {
                "certification": certification,
                "user_obj": certification.user,
                "title": self.title,
            },
        )

    def post(self, request, certification_id):
        """Handle form submission"""
        success = CertificationsServices.delete_certification(certification_id)
        if not success:
            messages.error(
                request, "Erreur lors de la suppression de la certification!"
            )
            return HttpResponse(status=400)
        messages.success(request, "Certification supprimée avec succès!")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})
