import logging
from wps.commandType import CommandType
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute



class WpsStatus(Model):
    class Meta:
        table_name = 'wpstatus'
        region = 'eu-central-1'
    user_name = UnicodeAttribute(hash_key=True)
    status = UnicodeAttribute()


class WpsRepository:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        if not WpsStatus.exists():
            logger.info("Creating table wpsstatus")
            WpsStatus.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    def add(self, command: dict):
        self.logger.info('adding %s..', command)
        user = command['user']
        status = command['status']
        WpsStatus(user_name=user, status=status).save()


    def get(self, command: dict):
        self.logger.info('getting %s..', command)
        users = command['users']
        return WpsStatus.batch_get(users)
