from openapi.utils import extend_schema_tags

tag = 'subuser'
path = tag
name = '子账号管理'

extend_schema_tags(
    tag,
    name,
    {
        'type': 'table_page',
        'init': {
            'path': '/api/v1/user/child_account/',
            'method': 'get'
        },
        'global': {
            'create': {
                'tag': 'subuser.create',
                'description': '添加子账号'
            }
        },
        'local': {
            'set': {
                'tag': 'subuser.set',
                'description': '设置为主账号'
            },
            'switch': {
                'tag': 'subuser.switch',
                'description': '进入该账号'
            },
            'delete': {
                'path': '/api/v1/user/child_account/',
                'method': 'delete'
            }
        }
    }
)

subuser_create_tag = 'subuser.create'
subuser_create_name = '创建子账号'

extend_schema_tags(
    subuser_create_tag,
    subuser_create_name
)

subuser_set_tag = 'subuser.set'
subuser_set_name = '创建子账号'

extend_schema_tags(
    subuser_set_tag,
    subuser_set_tag
)
