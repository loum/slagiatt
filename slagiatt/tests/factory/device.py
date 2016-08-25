import factory

import slagiatt.model
import slagiatt.common


class Device(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = slagiatt.model.Device
        sqlalchemy_session = slagiatt.common.SESSION
