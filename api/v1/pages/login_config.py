from openapi.utils import extend_schema_tags

tag = 'login_config'
path = tag
name = '登录配置'

extend_schema_tags(
    tag,
    name,
    {
        'type':'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/config/',
            'method': 'get'
        },
        'global': {
            'update': {
                'tag': 'login_config.update'
            }
        }
    }
)

login_config_update_tag = 'login_config.update'
login_config_update_name = '编辑登录配置'

extend_schema_tags(
    login_config_update_tag,
    login_config_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/config/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/config/',
                'method': 'patch'
            }
        }
    }
)