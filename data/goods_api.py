import flask
from flask import jsonify, make_response

from . import db_session
from .goods import Goods

blueprint = flask.Blueprint(
    'goods_api',
    __name__,
    template_folder='templates'
)


# Возвращение словаря со всеми товарами
@blueprint.route('/api/goods')
def get_goods():
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods).all()
    return jsonify(
        {
            'goods':
                [item.to_dict(only=('title', 'price', 'category.name'))
                 for item in goods]
        }
    )


# Возвращение словаря с информацией о конкретном товаре
@blueprint.route('/api/goods/<int:id>')
def get_product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Goods).get(id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'product': product.to_dict(only=(
                'title', 'about', 'price', 'category'))
        }
    )