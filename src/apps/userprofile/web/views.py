from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.userprofile.selectors.userprofile_selectors import get_userprofile_by_id


class UserProfileView(View):
    template_name = "userprofile/userprofile.html"

    def get(self, request, userprofile_id):
        userprofile = get_userprofile_by_id(userprofile_id)
        userprofile.navbar_url = reverse_lazy('userprofile:profile', kwargs={'userprofile_id': userprofile.id, })
        context = {
            "userprofile": userprofile
        }
        return render(request, self.template_name, context)
