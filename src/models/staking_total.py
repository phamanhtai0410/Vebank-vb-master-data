from pymodm import fields
from lib.model import BaseMG


class StakingTotalModel(BaseMG):
    class Meta:
        collection_name = 'staking_total'
        final = True
        ignore_unknown_fields = True

    _id = fields.ObjectIdField(primary_key=True)
    env = fields.CharField(blank=True, default='')
    staking_contract = fields.CharField(blank=True, default='')
    total = fields.FloatField(blank=True, default=0)




