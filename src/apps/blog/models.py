from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from config.settings import settings


# Create your models here.


class PostCategory(models.Model):
    """
    Catégorie de l'article
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_categories",
        help_text="Utilisateur propriétaire des catégories d'articles.",
    )
    name = models.CharField(max_length=100, help_text="Nom de la catégorie articles.")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date de création de la catégorie."
    )

    def __str__(self):
        return self.name


class PostTag(models.Model):
    """
    Tag de l'article
    """

    name = models.CharField(max_length=50, unique=True, help_text="Nom du tag")

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Article
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_articles",
        help_text="Utilisateur propriétaire des articles.",
    )
    title = models.CharField(max_length=200, help_text="Nom de l'article.")
    category = models.ForeignKey(
        PostCategory, on_delete=models.CASCADE, related_name="articles",
        help_text="Catégorie de l'article"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date de création de l'article"
    )
    published_at = models.DateField(
        null=True,
        blank=True,
        help_text="Date de publication de l'article"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Date de dernière mise à jour de l'article"
    )
    image = models.ImageField(
        upload_to="posts/images/", blank=True, null=True, help_text="Image de l'article"
    )
    tags = models.ManyToManyField(PostTag, blank=True, help_text="Tags de l'article")
    is_active = models.BooleanField(
        default=True, help_text="Statut du l'article (actif/inactif)"
    )
    description = CKEditor5Field(
        "Content",
        config_name="default",
        blank=True,
        help_text="Détails complets sur l'article.",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
