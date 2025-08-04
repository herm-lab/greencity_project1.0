from db.database import db

class User(db.Model):
    code = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_info = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.DateTime, server_default=db.func.now())
    waste_entries = db.relationship('WasteEntry', backref='user', lazy=True)