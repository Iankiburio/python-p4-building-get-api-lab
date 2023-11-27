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
    data = [{'id': bakery.id, 'name': bakery.name, 'created_at': bakery.created_at} for bakery in bakeries]
    return jsonify(data)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
       
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at
        }
        return jsonify(bakery_data), 200  
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    serialized_baked_goods = []
    
    for baked_good in baked_goods:
        serialized_baked_goods.append({
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format as needed
        })
    
    return jsonify(serialized_baked_goods), 200, {'Content-Type': 'application/json'}



@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        response_data = {
            'id': most_expensive.id,
            'name': most_expensive.name,
            'price': most_expensive.price,
            'created_at': most_expensive.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Convert to string if not a string
        }
        return jsonify(response_data), 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({'message': 'No baked goods found'}), 404, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(port=5555, debug=True)
