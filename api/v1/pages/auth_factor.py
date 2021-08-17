from openapi.utils import extend_schema_tags

tag = 'auth_factor_config'
path = "auth_factor"
name = '认证因素'

auth_factor_tag = 'auth_factor_config'
auth_factor_name = "认证因素列表"

extend_schema_tags(
    auth_factor_tag,
    auth_factor_name,
    {
        'type': 'table_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/authfactor/',
            'method': 'get'
        },
        # 'local': {
        #     'update': {
        #         'tag': 'auth_factor_config.update'
        #     },
        # },
        'global': {
            'create': {
                'tag': 'auth_factor_config.create'
            }
        }
    }
)


auth_factor_update_tag = 'auth_factor_config.update'
auth_factor_update_name = '编辑认证因素列表'

extend_schema_tags(
    auth_factor_update_tag,
    auth_factor_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/authfactor/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/authfactor/',
                'method': 'put'
            }
        }
    }
)


auth_factor_create_tag = 'auth_factor_config.create'
auth_factor_create_name = '添加认证因素'

extend_schema_tags(
    auth_factor_create_tag,
    auth_factor_create_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/authfactor_create/',
            'method': 'post'
        },
        'global': {
            'create': {
                'path': '/api/v1/tenant/{tenant_uuid}/authfactor_create/',
                'method': 'post'
            }
        }
    }
)