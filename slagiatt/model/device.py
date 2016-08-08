from slagiatt.shared.model import db


class Device(db.Model):
    equip_inst_id = db.Column(db.Integer, primary_key=True) 
    physical_name = db.Column(db.Unicode, unique=True)
    physical_name_extn = db.Column(db.Unicode)
    nw_ip_addr = db.Column(db.Unicode)
    equip_inst_id_1 = db.Column(db.Integer)
    equip_status_id = db.Column(db.Integer)
