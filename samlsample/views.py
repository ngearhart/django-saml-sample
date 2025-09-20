
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from onelogin.saml2.response import OneLogin_Saml2_Response
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from django_saml.views import saml_acs, prepare_django_request


class RootView(LoginRequiredMixin, TemplateView):
    """Render the Vue Root."""

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """Return information about the items to display on the homepage."""
        context = super().get_context_data(**kwargs)
        print(self.request.session.keys())
        context['saml_attrs'] = [{'key': key.replace("SAML_", ""), 'value': self.request.session[key]} for key in self.request.session.keys() if "SAML_" in key]
        return context


def mock_is_valid(self, request_data, request_id=None, raise_exceptions=False):
    return True


@never_cache
@csrf_exempt
def vulnerable_saml_acs(request):
    """Handle an AuthenticationResponse from the IdP."""

    OneLogin_Saml2_Response.is_valid = mock_is_valid

    # Add attributes to session
    req = prepare_django_request(request)
    saml_auth = OneLogin_Saml2_Auth(req, old_settings=settings.ONELOGIN_SAML_SETTINGS)
    request_id = request.session.get('AuthNRequestID', None)
    saml_auth.process_response(request_id=request_id)
    attrs = saml_auth.get_attributes()
    for key in attrs.keys():
        request.session[f'SAML_' + key] = attrs[key]

    return saml_acs(request)
