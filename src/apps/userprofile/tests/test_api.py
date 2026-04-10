# """
# Tests des APIs utilisateurs
#
# Objectifs :
# - Tester endpoint /me
# - Tester endpoint list users
# - Vérifier authentification requise
# - Vérifier sérialisation des données
# """
#
# from rest_framework.test import APITestCase
# from apps.users.models import User
#
#
# class UserApiTest(APITestCase):
#     """
#     Tests des endpoints API users
#     """
#
#     def setUp(self):
#         """Créer utilisateur et authentifier"""
#         self.user = User.objects.create_user(
#             email="api@test.com",
#             username="api",
#             password="password123"
#         )
#
#         self.client.force_authenticate(user=self.user)
#
#     def test_me_endpoint(self):
#         """GET /api/users/me/ doit retourner l'utilisateur connecté"""
#         response = self.client.get("/api/users/me/")
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["email"], "api@test.com")
#
#     def test_user_list(self):
#         """GET /api/users/ doit retourner la liste des utilisateurs"""
#         response = self.client.get("/api/users/")
#
#         self.assertEqual(response.status_code, 200)
