import pydash as py_
from pymodm import fields

from lib.enums.database import DBName
from lib.model import BaseMG
from lib.util import dt_utcnow
from lib.enums.database import DBName


class UsersModel(BaseMG):
    class Meta:
        collection_name = 'users'
        final = True
        ignore_unknown_fields = True

    _id = fields.ObjectIdField(primary_key=True)
    address = fields.CharField(blank=True, default='')
    hf = fields.FloatField(blank=True, default=0)
    pool_address = fields.CharField(blank=True, default='')
    last_action = fields.CharField(blank=True, default='')
    id_action = fields.CharField(blank=True, default='')

    is_liquidate = fields.BooleanField(blank=True, default=False)
    liquidate_log_id = fields.CharField(blank=True, default='')



