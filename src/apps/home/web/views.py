from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.blog.selectors.posts_selectors import PostSelectors
from apps.notifications.services.email_service import send_email
from apps.project.selectors.projects_selectors import ProjectSelectors
from apps.users.selectors.user_selectors import get_user_by_email
from apps.utils.services.http_responses import HTTPResponseHXRedirect


class HomePageView(View):
    """
    View for handling home page requests.
    """

    template_name = "home/home_page.html"

    def get(self, request):
        """
        Handle GET request for home page.
        Returns user data and project lists.
        """
        user_obj = get_user_by_email("kintymoustapha@gmail.com")

        if not user_obj:
            user_obj = type("UserMock", (), {})()
            user_obj.id = 1

        user_obj.navbar_url = reverse_lazy("home:home-page")

        user_obj.navbar_url = reverse_lazy("home:home-page")
        projects = (ProjectSelectors.get_projects())[:3]
        articles = (PostSelectors.get_posts())[:3]
        context = {
            "user_obj": user_obj,
            "projects": projects,
            "articles": articles,
        }
        return render(request, self.template_name, context)


class ContactPageView(View):
    """
    View for handling contact page requests.
    """

    template_name = "home/contact_page.html"

    def get(self, request):
        """
        Handle GET request for contact page.
        Returns contact form with user data.
        """
        user_obj = get_user_by_email("kintymoustapha@gmail.com")
        if not user_obj:
            user_obj = type("UserMock", (), {})()
            user_obj.id = 1
        contact = type("UserMock", (), {})()
        contact.navbar_url = reverse_lazy("home:contact-page")
        context = {"user_obj": user_obj, "contact": contact}
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Handle POST request for contact form submission.
        Validates input and sends email notification.
        """
        data = request.POST

        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        email = data.get("email", "")
        message = data.get("message", "")

        if not message or message == "":
            messages.error(request, "Merci de renseigner le message à envoyer")
            return HTTPResponseHXRedirect(reverse_lazy("home:contact-page"))

        send_email(
            subject="Contacte depuis votre site web",
            message=f"Prénom: {first_name}\n"
                    f"Nom: {last_name}\n"
                    f"Email: {email}\n"
                    f"\n{message}",
            recipients=["kintymoustapha@gmail.com"],
        )
        messages.success(request, "Message envoyé avec succès!")
        return HTTPResponseHXRedirect(reverse_lazy("home:home-page"))
