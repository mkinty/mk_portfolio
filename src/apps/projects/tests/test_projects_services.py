from django.test import TestCase
from apps.users.models import User
from apps.users.services import user_services


class UserServicesTestCase(TestCase):
    def setUp(self):
        """Setup initial data for tests."""
        self.first_name = "John"
        self.last_name = "Doe"
        self.email = "john.doe@example.com"
        self.password = "securepassword123"

    def test_create_user_account_creates_inactive_user(self):
        """Test that create_user_account creates a new inactive user."""
        user = user_services.create_user_account(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
        )

        # Check user instance
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.email, self.email)

        # Check user is inactive
        self.assertFalse(user.is_active)

        # Check password is hashed
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))

    def test_activate_user_account_sets_active_and_clears_token(self):
        """Test that activate_user_account activates user and clears token."""
        user = user_services.create_user_account(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
        )
        # set a dummy activation token
        user.activation_token = "123456"
        user.save()

        user_services.activate_user_account(user)

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertIsNone(user.activation_token)

    def test_set_user_password_changes_password(self):
        """Test that set_user_password correctly updates the password."""
        user = user_services.create_user_account(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
        )

        new_password = "new_secure_password"
        user_services.set_user_password(user, new_password)

        user.refresh_from_db()
        # Old password should fail
        self.assertFalse(user.check_password(self.password))
        # New password should work
        self.assertTrue(user.check_password(new_password))
