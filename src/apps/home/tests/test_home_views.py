import pytest
from django.contrib.messages import get_messages
from django.urls import reverse


@pytest.mark.django_db
class TestHomePageView:
    """
    Tests de la HomePageView
    """

    def test_home_page_returns_success_status(
        self,
        client,
        user_fixture,
        data_project_fixture,
        dev_project_fixture,
        monkeypatch,
    ):
        """
        Vérifie que la page d'accueil retourne un status 200.
        """

        monkeypatch.setattr(
            "apps.home.web.views.get_user_by_email", lambda email: user_fixture
        )

        response = client.get(reverse("home:home-page"))

        assert response.status_code == 200

    def test_home_page_uses_correct_template(
        self,
        client,
        user_fixture,
        data_project_fixture,
        dev_project_fixture,
        monkeypatch,
    ):
        """
        Vérifie que le bon template est utilisé.
        """

        monkeypatch.setattr(
            "apps.home.web.views.get_user_by_email", lambda email: user_fixture
        )

        response = client.get(reverse("home:home-page"))

        assert "home/home_page.html" in [
            template.name for template in response.templates
        ]

    def test_home_page_contains_context_data(
        self,
        client,
        user_fixture,
        data_project_fixture,
        dev_project_fixture,
        monkeypatch,
    ):
        """
        Vérifie les données envoyées au template.
        """

        monkeypatch.setattr(
            "apps.home.web.views.get_user_by_email", lambda email: user_fixture
        )

        response = client.get(reverse("home:home-page"))

        assert response.context["user_obj"].id == user_fixture.id
        assert "data_projects" in response.context
        assert "dev_projects" in response.context


@pytest.mark.django_db
class TestContactPageView:
    """
    Tests de la ContactPageView
    """

    def test_contact_page_get_returns_success_status(
        self, client, user_fixture, monkeypatch
    ):
        """
        Vérifie que la page contact retourne un status 200.
        """

        monkeypatch.setattr(
            "apps.home.web.views.get_user_by_email", lambda email: user_fixture
        )

        response = client.get(reverse("home:contact-page"))

        assert response.status_code == 200

    def test_contact_page_uses_correct_template(
        self, client, user_fixture, monkeypatch
    ):
        """
        Vérifie le template utilisé.
        """

        monkeypatch.setattr(
            "apps.home.web.views.get_user_by_email", lambda email: user_fixture
        )

        response = client.get(reverse("home:contact-page"))

        assert "home/contact_page.html" in [
            template.name for template in response.templates
        ]

    def test_contact_page_post_without_message_returns_error(self, client, monkeypatch):
        """
        Vérifie qu'une erreur est affichée si le message est vide.
        """

        response = client.post(
            reverse("home:contact-page"),
            data={
                "first_name": "Moustapha",
                "last_name": "KINTY",
                "email": "test@test.com",
                "message": "",
            },
        )

        assert response.status_code == 200

        messages = list(get_messages(response.wsgi_request))

        assert any(
            message.message == "Merci de renseigner le message à envoyer"
            for message in messages
        )

    def test_contact_page_post_send_email_success(self, client, monkeypatch):
        """
        Vérifie que l'email est envoyé correctement.
        """

        mocked_send_email = []

        def fake_send_email(subject, message, recipients):
            mocked_send_email.append(
                {
                    "subject": subject,
                    "message": message,
                    "recipients": recipients,
                }
            )

        monkeypatch.setattr("apps.home.web.views.send_email", fake_send_email)

        response = client.post(
            reverse("home:contact-page"),
            data={
                "first_name": "Moustapha",
                "last_name": "KINTY",
                "email": "test@test.com",
                "message": "Bonjour",
            },
        )

        assert response.status_code == 200

        assert len(mocked_send_email) == 1

        assert mocked_send_email[0]["subject"] == ("Contacte depuis votre site web")

        assert mocked_send_email[0]["recipients"] == ["kintymoustapha@gmail.com"]

        messages = list(get_messages(response.wsgi_request))

        assert any(
            message.message == "Message envoyé avec succès!" for message in messages
        )
