from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Q

from apps.tracking.selectors.applications_selectors import ApplicationSelectors, FollowUpSelectors
from apps.tracking.services.applications_services import ApplicationsServices, FollowUpServices
from apps.users.selectors.user_selectors import get_user_by_id


class ApplicationsTrackingIndexView(View):
    template_name = "tracking/applications_index.html"

    def get(self, request, user_id):
        user_obj = get_user_by_id(user_id)
        context = {
            "user_obj": user_obj
        }
        return render(request, self.template_name, context)


class ApplicationsTrackingView(View):
    template_name = "tracking/applications_tracking.html"

    def get(self, request, user_id):
        user_obj = get_user_by_id(user_id)

        applications = ApplicationSelectors.get_application_by_user(user_obj)

        application_status = request.GET.get('status')
        query = request.GET.get('qs', '')

        if application_status:
            applications = applications.filter(application_status=application_status)

        if query:
            applications = applications.filter(Q(position__icontains=query) | Q(company__icontains=query) | Q(
                job_offer_link__icontains=query)).distinct()

        # nombre de candidatures
        nb_applications = f"{len(applications)} Candidatures" if len(
            applications) > 1 else f"{len(applications)} Candidature"
        context = {
            "user_obj": user_obj,
            "applications": applications,
            "nb_applications": nb_applications
        }
        return render(request, self.template_name, context)


class JobApplicationAddView(View):
    """
    View for adding a new job application
    """

    template_name = "tracking/application_form.html"
    title = "Ajouter une candidature"

    def get(self, request, user_id):
        """
        GET request - Display the form to add a new job application
        """
        form, user_obj = ApplicationsServices.get_add_form(user_id)

        return render(request, self.template_name, {"form": form, "user_obj": user_obj, "title": self.title})

    def post(self, request, user_id):
        """
        POST request - Handle form submission to create a new job application
        """
        user_obj = get_user_by_id(user_id)

        success, form, user_obj = ApplicationsServices.create(
            user_obj,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {
                "form": form,
                "user_obj": user_obj,
                "title": self.title
            })

        messages.success(request, "Candidature ajoutée avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class JobApplicationUpdateView(View):
    """
    View for updating an existing job application
    """

    template_name = "tracking/application_form.html"
    title = "Modifier une candidature"

    def get(self, request, application_id):
        """
        GET request - Display the form to update a job application
        """
        form, application = ApplicationsServices.get_update_form(application_id)

        return render(request, self.template_name, {
            "form": form,
            "user_obj": application.user,
            "title": self.title
        })

    def post(self, request, application_id):
        """
        POST request - Handle form submission to update a job application
        """

        success, form, application = ApplicationsServices.update(
            application_id,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {
                "form": form,
                "user_obj": application.user,
                "title": self.title
            })

        messages.success(request, "Candidature modifiée avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class JobApplicationDeleteView(View):
    """
    View for deleting a job application
    """

    template_name = "tracking/application_delete_confirm.html"
    title = "Supprimer une candidature"

    def get(self, request, application_id):
        """
        GET request - Display the confirmation dialog for deleting a job application
        """
        application = ApplicationSelectors.get_application_by_id(application_id)

        return render(request, self.template_name, {"application": application, "title": self.title})

    def post(self, request, application_id):
        """
        POST request - Handle form submission to delete a job application
        """
        success = ApplicationsServices.delete(application_id)

        if not success:
            messages.error(request, "Erreur lors de la suppression de la candidature")
            return HttpResponse(status=400)

        messages.success(request, "Candidature supprimée avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ApplicationFollowUpAddView(View):
    """
    View for adding a follow-up to a job application
    """

    template_name = "tracking/followup_form.html"
    title = "Ajouter un suivi"

    def get(self, request, application_id):
        """
        GET request - Display the form to add a follow-up
        """
        form, application = FollowUpServices.get_add_form(application_id)

        return render(request, self.template_name, {
            "form": form,
            "application": application,
            "title": self.title
        })

    def post(self, request, application_id):
        """
        POST request - Handle form submission to add a follow-up
        """
        application = ApplicationSelectors.get_application_by_id(application_id)

        success, form, followup = FollowUpServices.create(
            application,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {"form": form, "title": self.title})

        messages.success(request, "Suivi ajouté avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ApplicationFollowUpUpdateView(View):
    """
    View for updating a follow-up to a job application
    """

    template_name = "tracking/followup_form.html"
    title = "Modifier un suivi"

    def get(self, request, followup_id):
        """
        GET request - Display the form to update a follow-up
        """
        form, followup = FollowUpServices.get_update_form(followup_id)

        return render(request, self.template_name, {
            "form": form,
            "followup": followup,
            "title": self.title
        })

    def post(self, request, followup_id):
        """
        POST request - Handle form submission to update a follow-up
        """
        success, form, followup = FollowUpServices.update(
            followup_id,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {"form": form, "title": self.title})

        messages.success(request, "Suivi modifié avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ApplicationFollowUpDeleteView(View):
    """
    View for deleting a follow-up to a job application
    """

    template_name = "tracking/followup_delete_confirm.html"
    title = "Supprimer un suivi"

    def get(self, request, followup_id):
        """
        GET request - Display the confirmation page for deleting a follow-up
        """
        followup = FollowUpSelectors.get_follow_up_by_id(followup_id)

        return render(request, self.template_name, {
            "followup": followup,
            "title": self.title
        })

    def post(self, request, followup_id):
        """
        POST request - Handle form submission to delete a follow-up
        """
        success = FollowUpServices.delete(followup_id)

        if not success:
            messages.error(request, "Erreur lors de la suppression du suivi")
            return HttpResponse(status=400)

        messages.success(request, "Suivi supprimé avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})
