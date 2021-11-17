from openapi.utils import extend_schema_tags

tag = 'extension'
path = tag
name = '插件配置'

extend_schema_tags(
    tag,
    name,
    {
        'type':'dashboard_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/',
            'method': 'get'
        },
        'global': {
            'create': {
                'to': 'marketplace',
                'description': '添加插件',
                'icon': 'el-icon-plus'
            }
        },
        'local': {
            'update': {
                'tag': 'extension.update',
                'description': '编辑',
                'icon': 'el-icon-edit'
            },
            'delete': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/{id}/',
                'method': 'delete',
                'description': '删除',
                'icon': 'el-icon-delete'
            }
        }
    }
)

extension_update_tag = 'extension.update'
extension_update_name = '编辑系统插件'

extend_schema_tags(
    extension_update_tag,
    extension_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/{id}/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/{id}/',
                'method': 'put',
                'description': '确定'
            }
        }
    }
)