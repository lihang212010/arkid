from openapi.utils import extend_schema_tags

tag = 'sdk'
path = tag
name = 'SDK下载'

extend_schema_tags(
    tag,
    name,
    {
        'type': 'table_page',
        'init': {
            'path': '/api/v1/sdk/',
            'method': 'get'
        },
        'local': {
            'read': {
                'tag': 'sdk.read',
                'description': '查看文档'
            }
        }
    }
)

sdk_read_tag = 'sdk.read'
sdk_read_name = '查阅'

extend_schema_tags(
    sdk_read_tag,
    sdk_read_name
)
