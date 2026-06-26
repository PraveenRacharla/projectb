from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "category": self.category,
            "amount": self.amount,
            "note": self.note
        }
