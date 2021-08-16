#!/usr/bin/env python3

from api.v1.views import data_sync as views_data_sync

from .tenant import tenant_router


tenant_external_idp_router = tenant_router.register(
    r'sync_config',
    views_data_sync.DataSyncConfigViewSet,
    basename='tenant-data-sync',
    parents_query_lookups=['tenant'],
)
