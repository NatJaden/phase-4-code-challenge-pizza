from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurant_dict = restaurant.to_dict()
        restaurants.append(restaurant_dict)

    response = make_response(restaurants, 200)
    return response

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'restaurant_pizzas': [rp.to_dict() for rp in restaurant.restaurant_pizzas]
        }
        return make_response(jsonify(restaurant_data), 200)
    else:
        return make_response(jsonify({"error": "Restaurant not found"}), 404) 

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        response = make_response('', 204)
    else:
        response = make_response({"error": "Restaurant not found"}, 404)
    return response

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = []
    for pizza in Pizza.query.all():
        pizza_dict = pizza.to_dict()
        pizzas.append(pizza_dict)

    response = make_response(pizzas, 200)
    return response

@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.json
    try:
        new_restaurant_pizza = RestaurantPizza(
            price=data["price"],
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"]
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify(new_restaurant_pizza.to_dict()), 201
    
    except ValueError as e:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)

if __name__ == "__main__":
    app.run(port=5555, debug=True)