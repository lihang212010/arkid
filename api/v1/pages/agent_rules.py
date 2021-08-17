from openapi.utils import extend_schema_tags

tag = 'agent_rules'
path = tag
name = '代理规则'

extend_schema_tags(
    tag,
    name,
    {
        'type':'table_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/agentrules/',
            'method': 'get'
        },
        'global': {
            'create': {
                'tag': 'agent_rules_create'
            }
        }
    }
)

agent_rule_create_tag = "agent_rules_create"
agent_rule_create_name = "添加代理规则"

extend_schema_tags(
    agent_rule_create_tag,
    agent_rule_create_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/agentrules_create/',
            'method': 'post'
        },
        'global': {
            'create': {
                'path': '/api/v1/tenant/{tenant_uuid}/agentrules_create/',
                'method': 'post'
            }
        }
    }
)