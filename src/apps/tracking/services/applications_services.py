from apps.tracking.forms import JobApplicationForm, ApplicationFollowUpForm
from apps.tracking.selectors.applications_selectors import ApplicationSelectors, FollowUpSelectors
from apps.users.selectors.user_selectors import get_user_by_id


class ApplicationsServices:
    """
    Services for job applications
    """

    @staticmethod
    def get_add_form(user_id):
        """Get the form for adding a new job application"""
        user = get_user_by_id(user_id)
        form = JobApplicationForm()
        return form, user

    @staticmethod
    def create(user, data, files):
        """Create a new job application"""
        form = JobApplicationForm(data, files)
        if not form.is_valid():
            return False, form, None
        application = form.save(commit=False)
        application.user = user
        application.save()
        return True, form, application

    @staticmethod
    def get_update_form(application_id):
        """Get the form for updating an existing job application"""
        application = ApplicationSelectors.get_application_by_id(application_id)
        if not application:
            return None, None
        form = JobApplicationForm(instance=application)
        return form, application

    @staticmethod
    def update(application_id, data, files):
        """Update an existing job application"""
        application = ApplicationSelectors.get_application_by_id(application_id)
        if not application:
            return False, None, None
        form = JobApplicationForm(data, files, instance=application)
        if not form.is_valid():
            return False, form, None
        form.save()
        return True, form, application

    @staticmethod
    def delete(application_id):
        """Delete an existing job application"""
        application = ApplicationSelectors.get_application_by_id(application_id)
        if not application:
            return False
        application.delete()
        return True


class ApplicationFollowUpServices:
    """
    Services for job application follow-ups
    """

    @staticmethod
    def get_add_form(application_id):
        """Get a form for adding a new follow-up"""
        application = ApplicationSelectors.get_application_by_id(application_id)
        if not application:
            return None, None
        form = ApplicationFollowUpForm()
        return form, application

    @staticmethod
    def create(application, data, files):
        """Create a new follow-up element"""
        form = ApplicationFollowUpForm(data, files)
        if not form.is_valid():
            return False, form, None
        follow_up = form.save(commit=False)
        follow_up.job_application = application
        follow_up.save()
        return True, form, follow_up

    @staticmethod
    def get_update_form(follow_up_id):
        """Get an update form for a follow-up element"""
        follow_up = FollowUpSelectors.get_follow_up_by_id(follow_up_id)
        if not follow_up:
            return None, None
        form = ApplicationFollowUpForm(instance=follow_up)
        return form, follow_up

    @staticmethod
    def update(follow_up_id, data, files):
        """Update a follow-up element"""
        follow_up = FollowUpSelectors.get_follow_up_by_id(follow_up_id)
        if not follow_up:
            return False, None, None
        form = ApplicationFollowUpForm(data, files, instance=follow_up)
        if not form.is_valid():
            return False, form, None
        form.save()
        return True, form, follow_up

    @staticmethod
    def delete(follow_up_id):
        """Delete a follow-up element"""
        follow_up = FollowUpSelectors.get_follow_up_by_id(follow_up_id)
        if not follow_up:
            return False
        follow_up.delete()
        return True
