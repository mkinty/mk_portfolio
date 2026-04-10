from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.users.selectors.user_selectors import get_user_by_email


class ProjectsView(View):
    template_name = "projects/projects_list.html"

    def get(self, request):
        mk = get_user_by_email("kintymoustapha@gmail.com")
        projects = mk
        projects.navbar_url = reverse_lazy('projects:projects-list')
        context = {
            "projects": projects,
        }
        return render(request, self.template_name, context)


class ProjectDetailView(View):
    template_name = "projects/project_detail.html"

    def get(self, request):
        mkprofile = get_user_by_email("kintymoustapha@gmail.com")
        projects = mkprofile
        projects.navbar_url = reverse_lazy('projects:project-detail')
        context = {
            "mkprofile": mkprofile,
            "projects": projects,
        }
        return render(request, self.template_name, context)