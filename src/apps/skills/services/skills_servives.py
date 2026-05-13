from apps.skills.forms import SkillsForm
from apps.skills.selectors.skills_selectors import SkillsSelectors
from apps.users.selectors.user_selectors import get_user_by_id


class SkillsService:
    """
    Service class for skills operations
    """

    @staticmethod
    def get_add_form(user_id):
        """Prepare form for adding a new skill"""
        user = get_user_by_id(user_id)
        form = SkillsForm()
        return form, user

    @staticmethod
    def create(user, data, files):
        """Create a new skill instance"""
        form = SkillsForm(data, files)
        if not form.is_valid():
            return False, form, None

        skill = form.save(commit=False)
        skill.user = user
        skill.save()

        return True, form, skill

    @staticmethod
    def get_update_form(skill_id):

        skill = SkillsSelectors.get_skill_by_id(skill_id)
        form = SkillsForm(instance=skill)
        return form, skill

    @staticmethod
    def update(skill_id, data, files):
        """Update an existing skill instance"""
        skill = SkillsSelectors.get_skill_by_id(skill_id)
        form = SkillsForm(data, files, instance=skill)

        if not form.is_valid():
            return False, form, skill

        form.save()
        return True, form, skill

    @staticmethod
    def delete(skill_id: int) -> bool:
        """Delete a skill instance"""
        skill = SkillsSelectors.get_skill_by_id(skill_id)
        if not skill:
            return False
        skill.delete()
        return True
