# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from apps.authentication.api.serializers import RegisterSerializer, LoginSerializer
#
#
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         token, _ = Token.objects.get_or_create(user=user)
#
#         return Response(
#             {"token": token.key}, status=status.HTTP_201_CREATED
#         )
#
#
# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         token, _ = Token.objects.get_or_create(user=user)
#
#         return Response({"token": token.key})
