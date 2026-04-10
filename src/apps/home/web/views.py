from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.users.selectors.user_selectors import get_user_by_email


class HomePageView(View):
    template_name = "home/home_page.html"


    def get(self, request):
        mk = get_user_by_email("kintymoustapha@gmail.com")
        mk.navbar_url = reverse_lazy('home:home-page')
        context = {
            "mk": mk,
        }
        return render(request, self.template_name, context)



class ContactPageView(View):
    template_name = "home/contact_page.html"


    def get(self, request):
        contact = get_user_by_email("kintymoustapha@gmail.com")
        contact.navbar_url = reverse_lazy('home:contact-page')
        context = {
            "contact": contact,
        }
        return render(request, self.template_name, context)