from typing import Optional

from apps.experiences.models import Experience


def get_experience_by_id(experience_id: int) -> Optional[Experience]:
    """
    Retrieve an experience by its unique identifier.

    Args:
        experience_id (int): ID of the experience.

    Returns:
        Optional[Experience]: The experience instance if found, otherwise None.
    """
    return Experience.objects.filter(pk=experience_id).first()


def get_all_experiences() -> list[Experience]:
    """
    Retrieve all experiences.

    Returns:
        list[Experience]: A list of all experience instances.
    """
    return Experience.objects.all()
