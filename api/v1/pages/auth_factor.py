from openapi.utils import extend_schema_tags

tag = 'auth_factor'
path = tag
name = '认证因素'

extend_schema_tags(
    tag,
    name
)