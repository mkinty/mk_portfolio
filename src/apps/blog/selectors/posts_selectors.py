from apps.blog.models import PostCategory, PostTag, Post


class PostCategorySelectors:
    """
    Selectors for PostCategory model
    """

    @staticmethod
    def get_post_category_by_id(post_category_id):
        """
        Get a post category by its ID
        """
        try:
            return PostCategory.objects.get(pk=post_category_id)
        except PostCategory.DoesNotExist:
            return None

    @staticmethod
    def get_post_categories():
        """
        Get all post categories
        """
        return PostCategory.objects.all()


class PostTagSelectors:
    """
    Selectors for PostTag model
    """

    @staticmethod
    def get_post_tag_by_id(tag_id):
        """
        Get a tag by its ID
        """
        try:
            return PostTag.objects.get(pk=tag_id)
        except PostTag.DoesNotExist:
            return None

    @staticmethod
    def get_post_tags():
        """
        Get all tags
        """
        return PostTag.objects.all()


class PostSelectors:
    """Selectors for Post model"""

    @staticmethod
    def get_post_by_id(project_id):
        """
        Get a post by its ID
        """
        try:
            return Post.objects.get(pk=project_id)
        except Post.DoesNotExist:
            return None

    @staticmethod
    def get_posts():
        """
        Get all posts
        """
        return Post.objects.all()

    @staticmethod
    def get_posts_by_category(category):
        """
        Get posts by category
        """
        return category.articles.all()

    @staticmethod
    def get_posts_by_user(user):
        """
        Get posts by user
        """
        return user.user_articles.all()

    @staticmethod
    def get_posts_by_tag(tag):
        """
        Get posts by tag (case-insensitive)
        """
        return Post.objects.filter(tags__name__iexact=str(tag).strip()).distinct()
