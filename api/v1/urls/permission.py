from api.v1.views import (
    permission as views_permission,
)

from .tenant import tenant_router


tenant_router.register(r'permission',
        views_permission.PermissionViewSet,
        basename='tenant-permission',
        parents_query_lookups=['tenant',])

tenant_router.register(r'permission_group',
        views_permission.PermissionGroupViewSet,
        basename='tenant-permission-group',
        parents_query_lookups=['tenant',])

tenant_router.register(r'permission_manage',
        views_permission.PermissionManageViewSet,
        basename='tenant-permission-manage',
        parents_query_lookups=['tenant',])
