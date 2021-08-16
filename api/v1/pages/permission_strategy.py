from openapi.utils import extend_schema_tags

tag = 'permission_strategy'
path = tag
name = '权限策略'

extend_schema_tags(
    tag,
    name
)