"""Middleware for redirecting unauthenticated users."""
# pylint: disable=no-self-use

import re

from django.conf import settings
from django.http import HttpResponseRedirect


EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [
        re.compile(exempt_url) for exempt_url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(object):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        """Process request and redirect user if they're unauthenticated."""
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if path == '':
                return
            if not any(m.match(path) for m in EXEMPT_URLS):
                redirect_to = '%s?next=%s' % (settings.LOGIN_URL,
                                              request.path_info)
                return HttpResponseRedirect(redirect_to)
