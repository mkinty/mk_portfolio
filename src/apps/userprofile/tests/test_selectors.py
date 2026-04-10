# """
# Tests des selectors users
#
# Objectifs :
# - Vérifier les requêtes d'accès aux données
# - Tester récupération par ID
# - Tester récupération par email
# - Tester récupération de tous les utilisateurs
# """
#
# from django.test import TestCase
# from apps.users.models import User
# from apps.users.selectors.user_selectors import (
#     get_all_users,
#     get_user_by_id,
#     get_user_by_email
# )
#
#
# class UserSelectorsTest(TestCase):
#     """
#     Tests des selectors User
#     """
#
#     def setUp(self):
#         """Créer un utilisateur pour les tests"""
#         self.user = User.objects.create_user(
#             email="selector@test.com",
#             username="selector",
#             password="password123"
#         )
#
#     def test_get_all_users(self):
#         """Doit retourner tous les utilisateurs"""
#         users = get_all_users()
#         self.assertEqual(users.count(), 1)
#
#     def test_get_user_by_id(self):
#         """Doit retourner un utilisateur via son ID"""
#         user = get_user_by_id(self.user.id)
#         self.assertEqual(user.email, "selector@test.com")
#
#     def test_get_user_by_email(self):
#         """Doit retourner un utilisateur via son email"""
#         user = get_user_by_email("selector@test.com")
#         self.assertEqual(user.username, "selector")
