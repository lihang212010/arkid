from openapi.utils import extend_schema_tags

tag = 'data_sync'
path = tag
name = '数据同步'


extend_schema_tags(
    tag,
    name,
    {
        'type': 'table_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/sync_config/',
            'method': 'get'
        },
        'global': {
            'create': {
                'tag': 'data_sync.create'
            }
        },
        'local': {
            'update': {
                'tag': 'data_sync.update'
            },
            'delete': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/sync_config/{id}/',
                'method': 'delete',
            },
        },
    },
)

data_sync_create_tag = 'data_sync.create'
data_sync_create_name = '创建数据同步配置'

extend_schema_tags(
    data_sync_create_tag,
    data_sync_create_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/sync_config/',
            'method': 'post',
        },
        'global': {
            'create': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/sync_config/',
                'method': 'post',
            }
        },
    },
)

data_sync_update_tag = 'data_sync.update'
data_sync_update_name = '编辑数据同步配置'

extend_schema_tags(
    data_sync_update_tag,
    data_sync_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/sync_config/{id}/',
            'method': 'get',
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/sync_config/{id}/',
                'method': 'put',
            }
        },
    },
)
