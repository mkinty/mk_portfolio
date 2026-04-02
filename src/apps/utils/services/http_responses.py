from django.http import HttpResponseRedirect


class HTTPResponseHXRedirect(HttpResponseRedirect):
    """
    Custom HTTP response for HTMX that triggers a client-side redirect.

    This class extends Django's HttpResponseRedirect and adds the
    "HX-Redirect" header, which HTMX can use to redirect the browser
    without requiring a full page reload. It also overrides the status
    code to 200 to indicate a successful HTMX request.

    Usage:
        return HTTPResponseHXRedirect("/target-url/")

    Attributes:
        status_code (int): HTTP status code, set to 200 for HTMX compatibility.

    Example:
        from django.views import View
        from apps.utils.services.http_responses import HTTPResponseHXRedirect

        class ExampleView(View):
            def post(self, request):
                # Some processing logic
                return HTTPResponseHXRedirect("/success/")
    """

    status_code = 200

    def __init__(self, *args, **kwargs):
        """
        Initialize the HTMX redirect response.

        Sets the "HX-Redirect" header to the value of "Location", which
        instructs HTMX to perform a client-side redirect.

        Args:
            *args: Positional arguments passed to HttpResponseRedirect.
            **kwargs: Keyword arguments passed to HttpResponseRedirect.
        """
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]
