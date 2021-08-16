from openapi.utils import extend_schema_tags

tag = 'tenant_register_privacy_notice'
path = 'register_config'
name = '注册配置'

tenant_register_privacy_notice_tag = 'tenant_register_privacy_notice'
tenant_register_privacy_notice_name = '注册隐私声明配置'

extend_schema_tags(
    tenant_register_privacy_notice_tag,
    tenant_register_privacy_notice_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/privacy_notice/',
            'method': 'get'
        },
        'global': {
            'update': {
                'tag': 'tenant_register_privacy_notice.update'
            }
        }
    }
)

tenant_register_privacy_notice_update_tag = 'tenant_register_privacy_notice.update'
tenant_register_privacy_notice_update_name = '编辑注册隐私声明配置'

extend_schema_tags(
    tenant_register_privacy_notice_update_tag,
    tenant_register_privacy_notice_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/privacy_notice/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/privacy_notice/',
                'method': 'put'
            }
        }
    }
)