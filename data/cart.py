import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Cart(SqlAlchemyBase):
    __tablename__ = 'cart'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    product_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'{self.id} {self.user_id} {self.product_id}'
