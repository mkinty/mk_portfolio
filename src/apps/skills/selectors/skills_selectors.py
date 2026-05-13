from apps.skills.models import Skills


class SkillsSelectors:
    """
    Selectors for the Skills model.
    """

    @staticmethod
    def get_all_skills(user):
        """Retrieve all skills for a user."""
        return user.skills.all()

    @staticmethod
    def get_skill_by_id(skill_id):
        """Retrieve an experience by its unique identifier."""
        try:
            return Skills.objects.get(pk=skill_id)
        except Skills.DoesNotExist:
            return None
