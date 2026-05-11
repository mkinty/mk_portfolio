from apps.tracking.models import JobApplication, ApplicationFollowUp


class ApplicationSelectors:
    """Selectors for JobApplication model"""

    @staticmethod
    def get_application_by_id(application_id):
        """Get job applications by company name"""
        try:
            return JobApplication.objects.get(pk=application_id)
        except JobApplication.DoesNotExist:
            return None

    @staticmethod
    def get_application_by_user(user):
        """Get job applications by user"""
        return (
            user.job_applications
            .all()
            .prefetch_related('follow_ups')
        )

    @staticmethod
    def get_application_by_status(status):
        """Get job applications by status"""
        return JobApplication.objects.filter(application_status=status)

    @staticmethod
    def get_all_applications():
        """Get all job applications"""
        return JobApplication.objects.all()


class FollowUpSelectors:
    """Selectors for follow-up tracking"""

    @staticmethod
    def get_follow_up_by_id(follow_up_id):
        """Get follow-up by ID"""
        try:
            return ApplicationFollowUp.objects.get(pk=follow_up_id)
        except ApplicationFollowUp.DoesNotExist:
            return None

    @staticmethod
    def get_follow_ups_by_application(application):
        """Get follow-ups for a specific application"""
        return application.follow_ups.all()
