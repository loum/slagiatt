"""SQLAlchemy class mapping for the Device route.
"""
import sqlalchemy

import slagiatt.common


class Device(slagiatt.common.BASE):
    """Model abstraction of a NBN device in the field.

    """
    __tablename__ = 'device'

    equip_inst_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    physical_name = sqlalchemy.Column(sqlalchemy.Unicode, unique=True)
    physical_name_extn = sqlalchemy.Column(sqlalchemy.Unicode)
    nw_ip_addr = sqlalchemy.Column(sqlalchemy.Unicode)
    equip_inst_id_1 = sqlalchemy.Column(sqlalchemy.Integer)
    equip_status_id = sqlalchemy.Column(sqlalchemy.Integer)
