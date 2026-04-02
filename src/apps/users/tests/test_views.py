# """
# Tests des vues Django (templates)
#
# Objectifs :
# - Vérifier que la page users s'affiche
# - Vérifier que les utilisateurs sont envoyés au template
# """
#
# from django.test import TestCase
# from apps.users.models import User
#
#
# class UserViewTest(TestCase):
#     """
#     Tests des vues HTML users
#     """
#
#     def setUp(self):
#         """Créer utilisateur"""
#         self.user = User.objects.create_user(
#             email="view@test.com",
#             password="password123"
#         )
#
#     def test_user_list_view(self):
#         """La page users doit s'afficher correctement"""
#         response = self.client.get("/users/")
#
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "view@test.com")
