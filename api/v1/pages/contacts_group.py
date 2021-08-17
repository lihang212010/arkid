from openapi.utils import extend_schema_tags

tag = 'contacts_group'
path = tag
name = '组的可见性'

extend_schema_tags(
    tag,
    name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/contactsconfig/group_visibility/',
            'method': 'get'
        },
        'global': {
            'update': {
                'tag': 'contacts_group_visibility.update'
            }
        }
    }
)

contacts_group_visibility_update_tag = 'contacts_group_visibility.update'
contacts_group_visibility_update_name = '编辑通讯录分组可见性'

extend_schema_tags(
    contacts_group_visibility_update_tag,
    contacts_group_visibility_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/contactsconfig/group_visibility/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/contactsconfig/group_visibility/',
                'method': 'put'
            }
        }
    }
)
