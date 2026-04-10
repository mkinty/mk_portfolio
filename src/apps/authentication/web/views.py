from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View

from apps.authentication.services.authentication_services import authenticate_user
from apps.authentication.services.password_reset_services import send_password_reset_email
from apps.authentication.services.registration_services import validate_registration_data, register_user
from apps.users.selectors.user_selectors import get_user_from_token, get_user_by_email
from apps.users.services.user_services import activate_user_account, set_user_password
from apps.utils.services.http_responses import HTTPResponseHXRedirect


class RegistrationView(View):
    """
    Handle user registration.

    This view displays the registration form and processes
    user account creation after validating input data.

    GET request:
        - Displays the registration form.

    POST request:
        - Retrieves form data
        - Validates user input.
        - Displays errors if validation fails
        - Creates user account if valid.
        - Redirects to home page on success.

    Template:
        "authentication/register.html"

    Messages:
        Success: "Votre compte a été créé avec succès"
        Error: "Erreur lors de la création du compte"
    """

    template_name = "authentication/register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request - display registration form"""
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle POST request - process registration form submission"""
        data = request.POST

        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        password2 = data.get("password2", "")

        errors = validate_registration_data(first_name, last_name, email, password, password2)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, self.template_name, {"data": data})

        domain = f"{'https' if request.is_secure() else 'http'}://{request.get_host()}"
        register_user(first_name, last_name, email, password, domain)

        messages.success(request, "Compte créé")
        print("Compte créé avec succès, un message d'activation a été envoyé à l'adresse email fournie")
        return HTTPResponseHXRedirect(reverse_lazy('home:home-page'))


class ActivateAccountView(View):
    """
    Handles account activation via a unique activation token.

    GET request:
        - Retrieves the user associated with the provided activation token.
        - Verifies token validity.
        - If valid, activates the user account and redirects to login.
        - If invalid or expired, displays an error message.
        - Redirects to home page on success.

    Template:
        "authentication/activate_account.html"

    Messages:
        Success: "Votre compte a été activé avec succès !"
        Error: "Lien d'activation invalide ou expiré"

    URL parameters:
        uidb64 (str): Base64 encoded user ID.
        token (str): Unique activation token sent via email.
    """
    template_name = "authentication/activate_account.html"

    def get(self, request, uidb64: str, token: str):
        """Handle GET request - verify token and activate account"""
        user = get_user_from_token(uidb64, token)

        if not user:
            messages.error(request, "Lien d'activation invalide ou expiré")
            return render(request, self.template_name)

        activate_user_account(user)
        messages.success(request, "Votre compte a été activé avec succès !")
        return redirect("home:home-page")


class PasswordResetRequestView(View):
    """
    Handles password reset requests.

    GET request:
        - Renders the password reset request form.

    POST request:
        - Receives the user's email.
        - Checks if a user exists with that email.
        - If yes, sends a password reset email.
        - If no, displays an error message.
        - Redirects to home page on success.

    Template:
        "authentication/password_reset_request.html"

    Messages:
        Success: "Un email pour réinitialiser votre mot de passe a été envoyé"
        Error: "Aucun compte trouvé avec cet email"
    """
    template_name = "authentication/password_reset_request.html"

    def get(self, request):
        """ Handle GET request - render password reset request form """
        return render(request, self.template_name)

    def post(self, request):
        """ Handle POST request - process password reset request """
        email = request.POST.get("email", "").strip()
        user = get_user_by_email(email)

        if not user:
            messages.error(request, "Aucun compte trouvé avec cet email")
            return render(request, self.template_name)

        domain = f"{'https' if request.is_secure() else 'http'}://{request.get_host()}"
        send_password_reset_email(user, domain)
        messages.success(request, "Un email pour réinitialiser votre mot de passe a été envoyé")
        return HTTPResponseHXRedirect(reverse_lazy('home:home-page'))


class PasswordResetConfirmView(View):
    """
    Handles password reset confirmation.

    GET request:
        - Verifies the token and displays the reset password form.
        - If the token is invalid or expired, shows an error.

    POST request:
        - Receives the new password and confirmation.
        - Validates password length and match.
        - Updates the user's password.
        - Redirects to home page on success.

    Template:
        "authentication/password_reset_confirm.html"

    Messages:
        Success: "Votre mot de passe a été réinitialisé avec succès"
        Error:
            - "Lien de réinitialisation invalide ou expiré"
            - "Les mots de passe ne correspondent pas"
            - "Le mot de passe doit comporter au moins 6 caractères"

    URL parameters:
        uidb64 (str): Base64-encoded user ID.
        token (str): Unique password reset token sent via email.
    """
    template_name = "authentication/password_reset_confirm.html"

    def get(self, request, uidb64: str, token: str):
        """ Handle GET request - verify token and display reset password form """
        user = get_user_from_token(uidb64, token)
        if not user:
            messages.error(request, "Lien de réinitialisation invalide ou expiré")
            return render(request, self.template_name)
        return render(request, self.template_name, {"uidb64": uidb64, "token": token})

    def post(self, request, uidb64: str, token: str):
        """ Handle POST request - process password reset confirmation """
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        user = get_user_from_token(uidb64, token)
        if not user:
            messages.error(request, "Lien de réinitialisation invalide ou expiré")
            return render(request, self.template_name)

        if password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, self.template_name, {"uidb64": uidb64, "token": token})

        if len(password) < 6:
            messages.error(request, "Le mot de passe doit comporter au moins 6 caractères")
            return render(request, self.template_name, {"uidb64": uidb64, "token": token})

        set_user_password(user, password)
        messages.success(request, "Votre mot de passe a été réinitialisé avec succès")
        return redirect("home:home-page")


class LoginView(View):
    """
    Handles user authentication.

    GET request:
        - Displays the login form.

    POST request:
        - Retrieves email and password from form.
        - Authenticates user using authentication service.
        - Logs the user in if credentials are valid.
        - Displays error message if authentication fails.

    Template:
        "authentication/login.html"

    Form fields:
        - email
        - password

    Messages:
        Success:
            "Connexion réussie"
        Error:
            "Email ou mot de passe incorrect"
            "Votre compte n'est pas encore activé"

    Redirect:
        - Success → home page
        - Failure → re-render login page
    """

    template_name = "authentication/login.html"

    def get(self, request):
        """ Handle GET request - display login form """
        return render(request, self.template_name)

    def post(self, request):
        """ Handle POST request - process login submission """
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        user = authenticate_user(email, password)
        if not user:
            messages.error(request, "Email ou mot de passe incorrect")
            return render(request, self.template_name)

        if not user.is_active:
            messages.error(request, "Votre compte n'est pas encore activé")
            return render(request, self.template_name)

        login(request, user)
        messages.success(request, "Connexion réussie")
        return HTTPResponseHXRedirect(reverse_lazy('home:home-page'))


class LogoutView(View):
    """
    Handles user logout.

    GET request:
        - Logs out the currently authenticated user.
        - Clears the session.
        - Redirects to home page.

    Messages:
        Success:
            "Vous êtes maintenant déconnecté"

    Redirect:
        - "home:home-page"
    """

    def get(self, request):
        """ Logout the current user."""
        logout(request)
        messages.success(request, "Vous êtes maintenant déconnecté")
        return HTTPResponseHXRedirect(reverse_lazy('home:home-page'))
