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
    restaurants = Restaurant.query.all()
    restaurants_list = [
        {
            'id' : restaurant.id,
            'address' : restaurant.address,
            'name' : restaurant.name
        }

        for restaurant in restaurants
    ]
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
            return {}, 204
        return make_response({
        " error": "Restaurant not found"
         }, 404)

    

@app.route('/pizzas')
def get_pizzas():
    pizzas = Pizza.query.all()
    pizzas_list = [
        {
            'id' : pizza.id,
            'ingredients' : pizza.ingredients,
            'name' : pizza.name
        }

        for pizza in pizzas
    ]
    return make_response(pizzas_list, 200)


@app.route('/restaurant_pizzas', methods=['POST'])
def get_rp():
    
    data = request.get_json()
    try:
        new_rp = RestaurantPizza(price=data["price"], pizza_id=data["pizza_id"], restaurant_id=data["restaurant_id"])
        db.session.add(new_rp)
        db.session.commit()
    except ValueError:
        error_message = {
            "errors": ["validation errors"]
        }
        return make_response(
            error_message,
            400
        )
    response = make_response(
            new_rp.to_dict(),
             201
            )
    return response
 

if __name__ == '__main__':
    app.run(port=5555, debug=True)

