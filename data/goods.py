import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Goods(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'goods'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('category.id'))
    picture_address = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    categories = orm.relationship("Category")

    def __repr__(self):
        return f'<Goods> {self.id} {self.title} {self.price} {self.category}'
