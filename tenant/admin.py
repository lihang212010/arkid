from django.contrib import admin
from .models import(
    Tenant, TenantConfig,
    TenantContactsConfig, TenantContactsUserFieldConfig, TenantContactsGroupConfig,
    TenantDesktopConfig, TenantSwitch,
)

admin.site.register(Tenant)
admin.site.register(TenantConfig)
# admin.site.register(TenantPasswordComplexity)
admin.site.register(TenantContactsConfig)
admin.site.register(TenantContactsUserFieldConfig)
admin.site.register(TenantContactsGroupConfig)
admin.site.register(TenantDesktopConfig)
admin.site.register(TenantSwitch)
