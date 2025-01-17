"""
SAML2.0协议登陆流程
"""
import logging
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.cache import never_cache
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from saml2 import BINDING_HTTP_POST
from saml2.authn_context import PASSWORD, AuthnBroker, authn_context_class_ref
from saml2.ident import NameID
from saml2.md import entity_descriptor_from_string
from saml2.s_utils import UnknownPrincipal, UnsupportedBinding
from saml2.saml import NAMEID_FORMAT_UNSPECIFIED
from djangosaml2idp.mxins import LoginRequiredMixin, IdPHandlerViewMixin
from app.models import App

logger = logging.getLogger(__name__)


@method_decorator(never_cache, name='dispatch')
class LoginProcess(LoginRequiredMixin, IdPHandlerViewMixin, View):
    """ View which processes the actual SAML request and returns a self-submitting form with the SAML response.
        The login_required decorator ensures the user authenticates first on the IdP using 'normal' ways.
    """

    def get(self, request, tenant__uuid, app_id):  # pylint: disable=unused-argument
        """SAML2.0协议登陆流程
        """
        binding = request.session.get('Binding', BINDING_HTTP_POST)

        app = App.active_objects.get(id=app_id)

        # Parse incoming request
        try:
            req_info = self.IDP.parse_authn_request(
                request.session['SAMLRequest'],
                binding
            )
        except Exception as excp:    # pylint: disable=broad-except
            return self.handle_error(request, exception=excp)
        # Signed request for HTTP-REDIRECT
        if "SigAlg" in request.session and "Signature" in request.session:
            _certs = self.IDP.metadata.certs(
                req_info.message.issuer.text, "any", "signing")
            verified_ok = False
            for cert in _certs:    # pylint: disable=unused-variable
                # TODO implement
                # if verify_redirect_signature(req_info, self.IDP.sec.sec_backend, cert):
                #    verified_ok = True
                #    break
                verified_ok = True
            if not verified_ok:
                return self.handle_error(request, extra_message="Message signature verification failure", status=400)
        # Gather response arguments
        try:
            resp_args = self.IDP.response_args(req_info.message)
        except (UnknownPrincipal, UnsupportedBinding) as excp:
            return self.handle_error(request, exception=excp, status=400)
        # print('resp_args is', resp_args)
        try:
            # sp_config = SAML_IDP_SPCONFIG[resp_args['sp_entity_id']]
            sp_config = {
                'processor': 'djangosaml2idp.processors.BaseProcessor',
                'attribute_mapping': {
                    'email': 'email',
                    'private_email': 'private_email',
                    'username': 'username',
                    'is_staff': 'is_staff',
                    'is_superuser': 'is_superuser',
                    'token': 'token',
                },
                'extra_config': app.data["attribute_mapping"]
            }
        except Exception:    # pylint: disable=broad-except
            return self.handle_error(request,
                                     exception=ImproperlyConfigured("No config for SP %s defined in SAML_IDP_SPCONFIG" %
                                                                    resp_args['sp_entity_id']),
                                     status=400)
        processor = self.get_processor(resp_args['sp_entity_id'], sp_config)

        # Check if user has access to the service of this SP
        if not processor.has_access(request):
            return self.handle_error(request,
                                     exception=PermissionDenied(
                                         "You do not have access to this resource"),
                                     status=403)
        cookie_user = request.user
        identity = self.get_identity(processor, cookie_user, sp_config)
        req_authn_context = req_info.message.requested_authn_context or PASSWORD
        # print('cookie_user is', cookie_user)
        # print('identity is', identity)
        # print('req_authn_context is', req_authn_context)
        AUTHN_BROKER = AuthnBroker()    # pylint: disable=invalid-name
        AUTHN_BROKER.add(authn_context_class_ref(req_authn_context), "")
        user_id = processor.get_user_id(cookie_user)
        # Construct SamlResponse message
        try:
            _spsso_descriptor = entity_descriptor_from_string(
                app.data["xmldata"]).spsso_descriptor.pop()  # pylint: disable=no-member
            
            policy = resp_args.get('name_id_policy', None)
            if policy is None:
                name_id_format = NAMEID_FORMAT_UNSPECIFIED
            else:
                name_id_format = policy.format

            idp_name_id_format_list = self.IDP.config.getattr("name_id_format", "idp") or [NAMEID_FORMAT_UNSPECIFIED]

            if name_id_format not in idp_name_id_format_list:
                raise ImproperlyConfigured(_('SP requested a name_id_format that is not supported in the IDP: {}').format(name_id_format))
            
            name_id = NameID(format=name_id_format, sp_name_qualifier=resp_args['sp_entity_id'], text=user_id)

            authn_resp = self.IDP.create_authn_response(
                identity=identity,
                userid=user_id,
                name_id=name_id,
                authn=AUTHN_BROKER.get_authn_by_accr(req_authn_context),
                sign_response=getattr(
                    _spsso_descriptor, 'want_response_signed', '') == 'true',
                sign_assertion=getattr(
                    _spsso_descriptor, 'want_assertions_signed', '') == 'true',
                **resp_args)
        except Exception as excp:    # pylint: disable=broad-except
            return self.handle_error(request, exception=excp, status=500)
        # print('authn_resp is', authn_resp)
        http_args = self.IDP.apply_binding(binding=resp_args['binding'],
                                           msg_str="%s" % authn_resp,
                                           destination=resp_args['destination'],
                                           relay_state=request.session['RelayState'],
                                           response=True)

        logger.debug('http args are: %s' %
                     http_args)    # pylint: disable=logging-not-lazy
        return self.render_response(request, processor, http_args)

    def render_response(self, request, processor, http_args):    # pylint: disable=no-self-use
        """
        Return either as redirect to MultiFactorView or as html with self-submitting form.
        """
        if processor.enable_multifactor(request.user):
            # Store http_args in session for after multi factor is complete
            request.session['saml_data'] = http_args['data']
            logger.debug("Redirecting to process_multi_factor")
            return HttpResponseRedirect(reverse('saml_multi_factor'))
        logger.debug("Performing SAML redirect")
        # return HttpResponseRedirect(http_args['headers'][0][1])
        return HttpResponse(http_args['data'])
