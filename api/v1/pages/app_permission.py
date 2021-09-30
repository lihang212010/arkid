from openapi.utils import extend_schema_tags

tag = [ 'app_list', 'apermission' ]
path = 'apermission'
name = '应用权限'

app_list_tag = 'app_list'
app_list_name = '所有应用'

extend_schema_tags(
    app_list_tag,
    app_list_name,
    {
        'type': 'tree_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/app_list/',
            'method': 'get',
            'next': 'apermission'
        },
        'node': {
            'next': 'apermission'
        }
    }
)

app_permission_tag = 'apermission'
app_permission_name = '该应用权限'

extend_schema_tags(
    app_permission_tag,
    app_permission_name,
    {
        'type': 'table_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/app_permission/{app_uuid}/',
            'method': 'get',
            'from': 'app_list'
        }
    }
)