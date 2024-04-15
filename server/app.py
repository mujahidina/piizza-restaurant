#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def get_restaurants():
    restaurants_list = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
    return make_response(restaurants_list, 200)


@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def get_by_id(id):
    if request.method == 'GET':
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            return make_response(restaurant.to_dict(), 200)
        return make_response({
        "error": "Restaurant not found"
        }, 404)
    

    elif request.method == 'DELETE':
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return {}, 200
        return make_response({
        " error": "Restaurant not found"
         }, 404)

    

@app.route('/pizzas')
def get_pizzas():
    pizza_list = [pizza.to_dict() for pizza in Pizza.query.all()]
    return make_response(pizza_list, 200)



@app.route('/restaurant_pizzas', methods=['GET', 'POST'])
def get_rp():

    if request.method == 'GET':
        restaurant_pizza_list = [restaurant_pizza.to_dict() for restaurant_pizza in RestaurantPizza.query.all()]
        return make_response(restaurant_pizza_list, 200)
    
    elif request.method == 'POST':
        new_rp = RestaurantPizza(
            price = request.json.get('price')
        )
        db.session.add(new_rp)
        db.session.commit()

        if new_rp:
            return make_response(new_rp.to_dict(), 200)
        return make_response({
        "errors": ["validation errors"]
        }, 404)
if __name__ == '__main__':
    app.run(port=5555, debug=True)
