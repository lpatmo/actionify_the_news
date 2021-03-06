"""Connect base url definitions."""
# pylint: disable=no-value-for-parameter,invalid-name
from urlparse import urljoin

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.views.generic import RedirectView, TemplateView
from django_bouncy.views import endpoint as bouncy_endpoint
import autocomplete_light

from open_connect.groups.views import GroupListView

autocomplete_light.autodiscover()
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', include('open_connect.welcome.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/',
        'django.contrib.auth.views.login',
        name='login'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        kwargs={'next_page': settings.POST_LOGOUT_PAGE},
        name='logout'),
    url(r'^accounts/', include('open_connect.accounts.urls')),
    url(r'^groups/', include('open_connect.groups.urls')),
    url(r'^messages/', include('open_connect.connectmessages.urls')),
    url(r'^moderation/', include('open_connect.moderation.urls')),
    url(r'^mail/bouncy/$',
        bouncy_endpoint,
        name='ses_endpoint'),
    url(r'^mail/', include('open_connect.mailer.urls')),
    url(r'^subscriptions/',
        include('open_connect.notifications.urls')),
    url(r'^media/', include('open_connect.media.urls')),
    url(r'^robots\.txt$',
        lambda r: HttpResponse(
            "User-agent: *\nDisallow: /", content_type="text/plain")),
    # pylint: disable=line-too-long
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url=urljoin(settings.STATIC_URL, 'img/favicon.ico'),
            permanent=True)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^reports/', include('open_connect.reporting.urls')),
    url(r'^explore/$', GroupListView.as_view(), name='explore'),
    url(r'^terms-and-conditions/$',
        TemplateView.as_view(template_name='terms_and_code_of_conduct.html'),
        name='terms_and_conditions'),
    url(r'^resources/', include('open_connect.resources.urls')),
    url('', include('social.apps.django_app.urls', namespace='social'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
