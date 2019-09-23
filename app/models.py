from app import db


class Task(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    md5 = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), nullable=False)