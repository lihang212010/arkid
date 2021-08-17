from openapi.utils import extend_schema_tags

tag = 'subadmin'
path = tag
name = '子管理员'

extend_schema_tags(
    tag,
    name,
    {
        'type': 'table_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/child_manager/',
            'method': 'get'
        },
        'global': {
            'create': {
                'tag': 'subadmin.create',
                'description': '添加新的子管理员'
            }
        },
        'local': {
            'update': {
                'tag': 'subadmin.update'
            },
            'delete': {
                'path': '/api/v1/tenant/{tenant_uuid}/child_manager/',
                'method': 'delete'
            }
        }
    }
)

subadmin_create_tag = 'subadmin.create'
subadmin_create_name = '添加新的子管理员'

extend_schema_tags(
    subadmin_create_tag,
    subadmin_create_name
)

subadmin_update_tag = 'subadmin.update'
subadmin_update_name = '编辑子管理员'

extend_schema_tags(
    subadmin_update_tag,
    subadmin_update_name
)