from app import db
from sqlalchemy.sql import func

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    name_en = db.Column(db.Text, nullable=False)
    name_ru = db.Column(db.Text)
    name_es = db.Column(db.Text)
    icon = db.Column(db.String(10))
    display_order = db.Column(db.Integer, default=0)
    is_premium = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def get_name(self, lang='en'):
        return getattr(self, f'name_{lang}', self.name_en) or self.name_en

    def to_dict(self, lang='en'):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.get_name(lang),
            'icon': self.icon,
            'is_premium': self.is_premium
        }
