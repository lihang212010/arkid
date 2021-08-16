from openapi.utils import extend_schema_tags

tag = 'device_manage'
path = tag
name = '设备管理'

extend_schema_tags(
    tag,
    name
)