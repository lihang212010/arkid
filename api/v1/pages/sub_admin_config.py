from openapi.utils import extend_schema_tags

tag = 'subadmin'
path = tag
name = '子管理员'

extend_schema_tags(
    tag,
    name
)