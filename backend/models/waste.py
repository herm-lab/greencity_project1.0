from db.database import db

class WasteEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_code = db.Column(db.String(6), db.ForeignKey('user.code'))
    waste_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    points_earned = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.DateTime, server_default=db.func.now())

class WasteType(db.Model):
    type = db.Column(db.String(20), primary_key=True)
    points_per_unit = db.Column(db.Integer, nullable=False)