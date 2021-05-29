from django.db import models
from common.model import BaseModel


class Schema(BaseModel):

    MAPPING_TYPE_CHOICES = (
        (0, 'None'),
        (1, 'Direct'),
        (2, 'Constant'),
        (3, 'Expression'), # Expression to be supported in ArkID
    )

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    mapping_type = models.IntegerField(choices=MAPPING_TYPE_CHOICES, default=0)
    default_value_if_is_none = models.CharField(max_length=128)
    source_attribute = models.CharField(max_length=256)
    target_attribute = models.CharField(max_length=256)
    is_used_matching = models.BooleanField(default=False)
    matching_precedence = models.IntegerField(blank=True, null=True, default=-1)

