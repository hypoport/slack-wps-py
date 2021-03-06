import logging

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class WpsStatus(Model):
    class Meta:
        table_name = 'wpstatus'
        region = 'eu-central-1'
        read_capacity_units = 1
        write_capacity_units = 1
    user_name = UnicodeAttribute(hash_key=True)
    from_date = UTCDateTimeAttribute()
    # from_date = UTCDateTimeAttribute(range_key=True)
    status = UnicodeAttribute()
    to_date = UTCDateTimeAttribute()


class WpsRepository:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        if not WpsStatus.exists():
            self.logger.info("Creating table wpstatus")
            WpsStatus.create_table(wait=True)

    def add(self, command: dict):
        self.logger.info('adding %s..', command)
        WpsStatus(user_name=(command['user']), status=(command['status']),
                  from_date=command['from_date'], to_date=command['to_date']).save()

    def get(self, command: dict):
        self.logger.info('getting %s..', command)
        users = command['users']
        return WpsStatus.batch_get(users)

    def clear(self, command):
        self.logger.info('clearing %s..', command)
        user = command['user']
        return WpsStatus(user_name=user).delete(condition=WpsStatus.user_name == user)
