from openapi.utils import extend_schema_tags

tag = 'find_password_config'
path = tag
name = '找回密码配置'

extend_schema_tags(
    tag,
    name
)