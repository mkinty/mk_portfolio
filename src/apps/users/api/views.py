from rest_framework import generics, permissions
from apps.users.models import User
from .serializers import UserSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer l'utilisateur connecté",
        description="Retourne les informations de l'utilisateur authentifié."
    ),
    put=extend_schema(
        summary="Mettre à jour l'utilisateur connecté",
        description="Met à jour les informations de l'utilisateur authentifié.",
        request=UserSerializer,
        responses=UserSerializer
    ),
    patch=extend_schema(
        summary="Modifier partiellement l'utilisateur connecté",
        description="Met à jour partiellement les informations de l'utilisateur authentifié.",
        request=UserSerializer,
        responses=UserSerializer
    ),
)
class MeView(generics.RetrieveUpdateAPIView):
    """
    Endpoint permettant de récupérer et modifier
    les informations de l'utilisateur connecté.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    summary="Liste des utilisateurs",
    description="Retourne la liste complète des utilisateurs (authentification requise).",
    responses=UserSerializer(many=True)
)
class UserListView(generics.ListAPIView):
    """
    Endpoint permettant de récupérer la liste
    de tous les utilisateurs.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
