from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import *

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):  # automatic calling the dict (creating a func)
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/all")
def all_cafes():
    cafes = db.session.query(Cafe).all()
    every_cafe = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafes=every_cafe)


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).get(cafe_id)
    print(cafe)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    delete_cafe = Cafe.query.get(cafe_id)
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        db.session.delete(delete_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe from the API."}), 200

    elif not delete_cafe:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403



@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/search")
def search_cafe():
    query_location = request.args.get("loc")
    cafe = Cafe.query.filter_by(location=query_location).all()
    if len(cafe) >= 1:
        return jsonify(cafes=[caf.to_dict() for caf in cafe])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route("/random")
def get_random_cafe():
    cafes = Cafe.query.all()  # or #  db.session.query(Cafe).all()
    random_cafe = choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())  # automatic calling the dict

    # return jsonify(cafe={          # manually doing it
    #     # "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #     "coffee_price": random_cafe.coffee_price,
    #     "amenities": {
    #         "has_toilet": random_cafe.has_toilet,
    #         "has_wifi": random_cafe.has_wifi,
    #         "seats": random_cafe.seats,
    #         "has_sockets": random_cafe.has_sockets,
    #         "can_take_calls": random_cafe.can_take_calls,
    #     }}
    # )


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)

    # searched_cafes = []
    # for cafe in cafes:
    #     if cafe.name == name:
    #         searched_cafes.append(cafe)
