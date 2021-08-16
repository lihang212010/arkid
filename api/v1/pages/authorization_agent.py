from openapi.utils import extend_schema_tags

tag = 'authorization_agent'
path = tag
name = '身份源代理'

extend_schema_tags(
    tag,
    name,
    {
        'type':'table_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/authorization_agent/',
            'method': 'get'
        }
    }
)