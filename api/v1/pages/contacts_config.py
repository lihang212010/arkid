from openapi.utils import extend_schema_tags

tag = [ 'contacts_switch', 'contacts_group_visibility', 'contacts_info_visibility' ]
path = 'contacts_config'
name = '通讯录设置'

contacts_switch_tag = 'contacts_switch'
contacts_switch_name = '通讯录开关'

extend_schema_tags(
    contacts_switch_tag,
    contacts_switch_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/contactsconfig/function_switch/',
            'method': 'get'
        },
        'global': {
            'update': {
                'tag': 'contacts_switch.update'
            }
        }
    }
)

contacts_switch_update_tag = 'contacts_switch.update'
contacts_switch_update_name = '编辑通讯录开关'

extend_schema_tags(
    contacts_switch_update_tag,
    contacts_switch_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/contactsconfig/function_switch/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/contactsconfig/function_switch/',
                'method': 'put'
            }
        }
    }
)

contacts_group_visibility_tag = 'contacts_group_visibility'
contacts_group_visibility_name = '通讯录分组可见性'

extend_schema_tags(
    contacts_group_visibility_tag,
    contacts_group_visibility_name,
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

contacts_info_visibility_tag = 'contacts_info_visibility'
contacts_info_visibility_name = '通讯录个人字段可见性'

extend_schema_tags(
    contacts_info_visibility_tag,
    contacts_info_visibility_name,
    {
        'type': 'table_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/contactsconfig/info_visibility/',
            'method': 'get'
        },
        'local': {
            'update': {
                'tag': 'contacts_info_visibility.update'
            }
        }
    }
)

contacts_info_visibility_update_tag = 'contacts_info_visibility.update'
contacts_info_visibility_update_name = '编辑通讯录个人字段可见性'

extend_schema_tags(
    contacts_info_visibility_update_tag,
    contacts_info_visibility_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/contactsconfig/info_visibility/{info_uuid}/detail/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/contactsconfig/info_visibility/{info_uuid}/detail/',
                'method': 'put'
            }
        }
    }
)