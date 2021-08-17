from api.v1.views import (
    tenant as views_tenant,
)
from rest_framework_extensions.routers import ExtendedSimpleRouter
from django.urls import re_path


router = ExtendedSimpleRouter()
tenant_router = router.register(
    r'tenant', views_tenant.TenantViewSet, basename='tenant'
)

urlpatterns = [
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/config/',
            views_tenant.TenantConfigView.as_view(), name='tenant-config'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/password_complexity/(?P<complexity_uuid>[\w-]+)/detail/',
            views_tenant.TenantPasswordComplexityDetailView.as_view(), name='tenant-password-complexity-detail'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/password_complexity/',
            views_tenant.TenantPasswordComplexityView.as_view(), name='tenant-password-complexity'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/current_password_complexity/',
            views_tenant.TenantCurrentPasswordComplexityView.as_view(), name='tenant-current-password-complexity'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/contactsconfig/function_switch/',
            views_tenant.TenantContactsConfigFunctionSwitchView.as_view(), name='tenant-contactsconfig-function-switch'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/desktopconfig/',
            views_tenant.TenantDesktopConfigView.as_view(), name='tenant-desktop-config'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/authfactor/',
            views_tenant.TenantAuthRefactorView.as_view(), name='tenant-authfactor'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/agentrules/',
            views_tenant.TenantAgentRuleView.as_view(), name='tenant-agentrules'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/agentrules_create/',
            views_tenant.TenantAgentRuleCreateView.as_view(), name='tenant-agentrules_create'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/authrules/',
            views_tenant.TenantAuthRuleView.as_view(), name='tenant-authrules'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/authrules_create/',
            views_tenant.TenantAuthRuleCreateView.as_view(), name='tenant-authrules_create'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/authfactor_create/',
            views_tenant.TenantAuthRefactorCreateView.as_view(), name='tenant-authfactor_create'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/authfactor_update',
            views_tenant.TenantAuthRefactorUpdateView.as_view(), name='tenant-authfactor_update'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/password_config/',
            views_tenant.TenantPasswordConfigView.as_view(), name='tenant-password-config'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/userprofileconfig/',
            views_tenant.TenantUserProfileConfigView.as_view(), name='tenant-user-profile-config'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/contactsconfig/info_visibility/(?P<info_uuid>[\w-]+)/detail/',
            views_tenant.TenantContactsConfigInfoVisibilityDetailView.as_view(), name='tenant-contactsconfig-info-visibility-detail'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/contactsconfig/info_visibility/',
            views_tenant.TenantContactsConfigInfoVisibilityView.as_view(), name='tenant-contactsconfig-info-visibility'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/contactsconfig/group_visibility/',
            views_tenant.TenantContactsConfigGroupVisibilityView.as_view(), name='tenant-contactsconfig-group-visibility'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/contacts/group/',
            views_tenant.TenantContactsGroupView.as_view(), name='tenant-contacts-group'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/contacts/user/',
            views_tenant.TenantContactsUserView.as_view(), name='tenant-contacts-user'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/contacts/user_tags/',
            views_tenant.TenantContactsUserTagsView.as_view(), name='tenant-contacts-user-tags'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/privacy_notice/',
            views_tenant.TenantPrivacyNoticeView.as_view(), name='tenant-privacy_notice'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/device/(?P<device_uuid>[\w-]+)/detail/',
            views_tenant.TenantDeviceDetailView.as_view(), name='tenant-device-detail'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/device_export/',
            views_tenant.TenantDeviceExportView.as_view(), name='tenant-device-export'),
    re_path(r'^tenant/(?P<tenant_uuid>[\w-]+)/device/',
            views_tenant.TenantDeviceListView.as_view(), name='tenant-device'),
    re_path(r'^tenant/(?P<slug>[\w-]+)/slug/$',
        views_tenant.TenantSlugView.as_view(), name='tenant-slug'),
]
