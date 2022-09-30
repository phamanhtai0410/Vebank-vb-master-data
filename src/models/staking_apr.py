from pymodm import fields
from lib.model import BaseMG


class StakingAPRModel(BaseMG):
    class Meta:
        collection_name = 'staking_apr'
        final = True
        ignore_unknown_fields = True

    _id = fields.ObjectIdField(primary_key=True)
    env = fields.CharField(blank=True, default='')
    staking_contract = fields.CharField(blank=True, default='')
    apr = fields.FloatField(blank=True, default=0)
    year = fields.IntegerField(blank=True, default=1970),
    month = fields.IntegerField(blank=True, default=1)
    day = fields.IntegerField(blank=True, default=1)



