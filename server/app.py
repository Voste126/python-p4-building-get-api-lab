#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [{"id": bakery.id, "name": bakery.name} for bakery in bakeries]
    response = make_response(
        jsonify(bakery_list),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        bakery_info = {"id": bakery.id, "name": bakery.name}
        response = make_response(jsonify(bakery_info))
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        return jsonify({"message": "Bakery not found"}), 404
    


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [{"id": baked_good.id, "name": baked_good.name, "price": baked_good.price} for baked_good in baked_goods]
    response = make_response(
        jsonify(baked_goods_list),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive_baked_good:
        baked_good_info = {"id": most_expensive_baked_good.id, "name": most_expensive_baked_good.name, "price": most_expensive_baked_good.price}
        response = make_response(jsonify(baked_good_info))
        return response
    else:
        return jsonify({"message": "No baked goods found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
