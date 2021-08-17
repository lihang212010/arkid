from openapi.utils import extend_schema_tags

tag = 'api_document'
path = tag
name = 'API文档'

extend_schema_tags(
    tag,
    name,
    {
        'type': 'html',
        'init': {
            'path': '/api/schema/redoc/',
            'method': 'get'
        }
    }
)