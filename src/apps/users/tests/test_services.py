# """
# Tests des services users
#
# Objectifs :
# - Tester la logique métier indépendante des vues
# - Tester la création d'utilisateur via service
# - Tester la mise à jour du profil utilisateur
# """
#
# from django.test import TestCase
# from apps.users.models import User
# from apps.users.services.user_service import create_user_account
#
#
# class UserServiceTest(TestCase):
#     """
#     Tests unitaires des services utilisateur
#     """
#
#     def test_create_user(self):
#         """Le service create_user doit créer un utilisateur"""
#         user = create_user_account(
#             email="service@test.com",
#             password="password123",
#             first_name="Service",
#             last_name="User",
#         )
#
#         self.assertIsInstance(user, User)
#
#
