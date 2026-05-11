from django.shortcuts import render
from django.views import View

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

        # nombre de candidatures
        # nb_applications = f"{len(projects)} Candidatures" if len(projects) > 1 else f"{len(projects)} Candidature"
        context = {
            "user_obj": user_obj
        }
        return render(request, self.template_name, context)
