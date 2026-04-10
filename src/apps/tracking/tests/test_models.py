# """
# Tests du modèle User
#
# Objectifs :
# - Vérifier la création d'un utilisateur
# - Vérifier la configuration USERNAME_FIELD (email)
# - Vérifier la méthode __str__
# - Vérifier le hash du mot de passe
# """
#
# from django.test import TestCase
# from apps.users.models import User
#
#
# class UserModelTest(TestCase):
#     """
#     Tests unitaires du modèle User
#     """
#
#     def test_create_user(self):
#         """Doit créer un utilisateur avec email comme identifiant"""
#         user = User.objects.create_user(
#             email="test@test.com",
#             username="test",
#             password="password123"
#         )
#
#         self.assertEqual(user.email, "test@test.com")
#         self.assertTrue(user.check_password("password123"))
#
#     def test_str_method(self):
#         """La méthode __str__ doit retourner 'first_name last_name'"""
#         user = User.objects.create_user(
#             email="test@test.com",
#             username="test",
#             first_name="John",
#             last_name="Doe",
#             password="password123"
#         )
#
#         self.assertEqual(str(user), "John Doe")