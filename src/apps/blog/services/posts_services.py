from apps.blog.forms import PostCategoryForm, PostForm, PostTagForm
from apps.blog.selectors.posts_selectors import (
    PostCategorySelectors,
    PostSelectors,
    PostTagSelectors,
)
from apps.users.selectors.user_selectors import get_user_by_id


class PostCategoryServices:
    """
    Service class for post category operations.
    """

    @staticmethod
    def get_add_form(user_id):
        """
        Get the form for adding a new post category.
        """
        user = get_user_by_id(user_id)
        form = PostCategoryForm()
        return form, user

    @staticmethod
    def create(user, data, files):
        """
        Create a new post category.
        """
        form = PostCategoryForm(data, files)
        if not form.is_valid():
            return False, form, None
        category = form.save(commit=False)
        category.user = user
        category.save()
        return True, form, category

    @staticmethod
    def get_update_form(category_id):
        """
        Get the form for updating an existing post category.
        """
        category = PostCategorySelectors.get_post_category_by_id(category_id)
        form = PostCategoryForm(instance=category)
        return form, category

    @staticmethod
    def update(category_id, data, files):
        """
        Update an existing post category.
        """
        category = PostCategorySelectors.get_post_category_by_id(category_id)
        form = PostCategoryForm(data, files, instance=category)
        if not form.is_valid():
            return False, form, category
        form.save()
        return True, form, category

    @staticmethod
    def delete(category_id):
        """
        Delete an existing post category.
        """
        category = PostCategorySelectors.get_post_category_by_id(category_id)
        if not category:
            return False
        category.delete()
        return True


class PostTagServices:
    """
    Service class for post tag operations.
    """

    @staticmethod
    def get_add_form():
        """
        Get the form for adding a new post tag.
        """
        form = PostTagForm()
        return form

    @staticmethod
    def create(data, files):
        """
        Create a new post tag.
        """
        form = PostTagForm(data, files)
        if not form.is_valid():
            return False, form, None
        tag = form.save()
        return True, form, tag

    @staticmethod
    def get_update_form(tag_id):
        """
        Get the form for updating an existing post tag.
        """
        tag = PostTagSelectors.get_post_tag_by_id(tag_id)
        form = PostTagForm(instance=tag)
        return form, tag

    @staticmethod
    def update(tag_id, data, files):
        """
        Update an existing post tag.
        """
        tag = PostTagSelectors.get_post_tag_by_id(tag_id)
        form = PostTagForm(data, files, instance=tag)
        if not form.is_valid():
            return False, form, tag
        form.save()
        return True, form, tag

    @staticmethod
    def delete(tag_id):
        """
        Delete an existing post tag.
        """
        tag = PostTagSelectors.get_post_tag_by_id(tag_id)
        if not tag:
            return False
        tag.delete()
        return True


class PostServices:
    """
    Service class for post operations.
    """

    @staticmethod
    def get_add_form(user_id):
        """
        Get the form for adding a new post.
        """
        user = get_user_by_id(user_id)
        form = PostForm()
        return form, user

    @staticmethod
    def create(user, data, files):
        """
        Create a new post.
        """
        form = PostForm(data, files)
        if not form.is_valid():
            return False, form, None
        post = form.save(commit=False)
        post.user = user
        post.save()
        form.save_m2m()  # Save many-to-many relationships
        return True, form, post

    @staticmethod
    def get_update_form(post_id):
        """
        Get the form for updating an existing post.
        """
        post = PostSelectors.get_post_by_id(post_id)
        form = PostForm(instance=post)
        return form, post

    @staticmethod
    def update(post_id, data, files):
        """
        Update an existing post.
        """
        post = PostSelectors.get_post_by_id(post_id)
        form = PostForm(data, files, instance=post)
        if not form.is_valid():
            return False, form, post
        form.save()
        return True, form, post

    @staticmethod
    def delete(post_id):
        """
        Delete an existing post.
        """
        post = PostSelectors.get_post_by_id(post_id)
        if not post:
            return False
        post.delete()
        return True
