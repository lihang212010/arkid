from openapi.utils import extend_schema_tags

tag = 'marketplace'
path = tag
name = '插件市场'

extend_schema_tags(
    tag,
    name,
    {
        'type':'dashboard_page',
        'init': {
            'path': '/api/v1/marketplace/',
            'method': 'get'
        },
        'local': {
            'install': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/{id}/',
                'method': 'put',
                'description': '点击安装'
            }
        }
    }
)