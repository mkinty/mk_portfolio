
from django.shortcuts import render
from django.views import View

from apps.authentication.services.authentication import authenticate_user
from apps.users.selectors.user import get_user_by_email, get_all_users


class HomePageView(View):
    template_name = "home/home_page.html"


    def get(self, request):
        mk = get_user_by_email("kintymoustapha@gmail.com")
        context = {
            "mk": mk
        }
        return render(request, self.template_name, context)
