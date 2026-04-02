# from rest_framework import serializers
# from apps.users.models import User
# from django.contrib.auth import authenticate
#
#
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ["email", "username", "password"]
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
#
#
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
#
#     def validate(self, data):
#         user = authenticate(
#             username=data["email"], password=data["password"]
#         )
#         if not user:
#             raise serializers.ValidationError("Invalid credentials")
#         return user
