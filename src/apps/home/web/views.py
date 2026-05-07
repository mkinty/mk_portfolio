from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.project.selectors.projects_selectors import TagSelectors, ProjectCategorySelectors, ProjectSelectors
from apps.users.selectors.user_selectors import get_user_by_email


class HomePageView(View):
    template_name = "home/home_page.html"

    def get(self, request):
        user_obj = get_user_by_email("kintymoustapha@gmail.com")
        user_obj.navbar_url = reverse_lazy('home:home-page')
        data_projects = (
            ProjectSelectors
            .get_projects_by_tag("Data")
            .select_related("category", "user")
            .prefetch_related("tags")
            .distinct()[:3]
        )
        dev_projects = (
            ProjectSelectors
            .get_projects_by_tag("Development")
            .select_related("category", "user")
            .prefetch_related("tags")
            .distinct()[:3]
        )
        context = {
            "user_obj": user_obj,
            "data_projects": data_projects,
            "dev_projects": dev_projects,
        }
        return render(request, self.template_name, context)


class ContactPageView(View):
    template_name = "home/contact_page.html"

    def get(self, request):
        user_obj = get_user_by_email("kintymoustapha@gmail.com")
        contact = dict()
        contact["navbar_url"] = reverse_lazy('home:contact-page')
        context = {
            "user_obj": user_obj,
            "contact": contact
        }
        return render(request, self.template_name, context)
