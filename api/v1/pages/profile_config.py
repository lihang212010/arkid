from openapi.utils import extend_schema_tags

tag = 'profile_config'
path = tag
name = '个人资料设置'

extend_schema_tags(
    tag,
    name,
    {
        "type": "form_page",
        "init": {
            'path': '/api/v1/tenant/{tenant_uuid}/userprofileconfig/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/userprofileconfig/',
                'method': 'put'
            }
        }
    }
)