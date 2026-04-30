from django.http import HttpResponseRedirect


class HTTPResponseHXRedirect(HttpResponseRedirect):
    """
    Custom HTTP response for HTMX that triggers a client-side redirect.

    Usage:
        return HTTPResponseHXRedirect("/target-url/")

    Attributes:
        status_code (int): HTTP status code, set to 200 for HTMX compatibility.
    """

    status_code = 200

    def __init__(self, *args, **kwargs):
        """
        Initialize the HTMX redirect response.

        Args:
            *args: Positional arguments passed to HttpResponseRedirect.
            **kwargs: Keyword arguments passed to HttpResponseRedirect.
        """
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]
