# Generated by hanbin 3.8 on 2021-06-24 03:30

from django.db import migrations

class Migration(migrations.Migration):

    def add_default_data(apps, schema_editor):
        pass
        # from tenant.models import Tenant, TenantContactsConfig
        # tenants = Tenant.active_objects.all()
        # for tenant in tenants:
        #     # 功能开关
        #     TenantContactsConfig.objects.get_or_create(
        #         is_del=False,
        #         tenant=tenant,
        #         data={
        #             "is_open": True
        #         }
        #     )
       

    dependencies = [
        ('tenant', '0012_tenantcontactsconfig'),
    ]

    operations = [
        migrations.RunPython(add_default_data),
    ]
