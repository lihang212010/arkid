from openapi.utils import extend_schema_tags

tag = ['auth_factor_config','auth_factor_password_config']
path = "auth_factor"
name = '认证因素'

auth_factor_tag="auth_factor_config"
auth_factor_name="认证因素列表"

extend_schema_tags(
    auth_factor_tag,
    auth_factor_name,
    {
        "type": "table_page",
        "init": {
            'path': '/api/v1/tenant/{tenant_uuid}/authfactor/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/authfactor/',
                'method': 'put'
            },
        }
    }
)

password_tag="auth_factor_password_config"
password_name="密码配置"

extend_schema_tags(
    password_tag,
    password_name,
    {
        "type": "form_page",
        "init": {
            'path': '/api/v1/tenant/{tenant_uuid}/password_config/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/password_config/',
                'method': 'put'
            }
        }
    }
)