from flask import Blueprint, jsonify, request, make_response, abort 
from app.models.planets import Planet
from app import db 

## WAVE 2
# class Planet:
#     def __init__(self, id, name, description, distance_from_sun):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.distance_from_sun = distance_from_sun


# list of planets
# planets = [
#     Planet(1, "Earth", "A planet were humans live", 92.96),
#     Planet(2, "Mercury", "Smallest planet in the solar system", 30.325),
#     Planet(3, "Venus", "It's named after Roman goddess of love and beauty", 67.24)
    
# ]

### WAVE 3 
#Blueprint
planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["POST"])
def create_one_planet():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"], 
                        description=request_body["description"],
                        miles_from_sun=request_body["miles_from_sun"])

    db.session.add(new_planet)
    db.session.commit()

    return {
        "id": new_planet.id,
        "msg": f"Successfully created planet with id {new_planet.id}"
    }, 201 

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    planets = Planet.query.all()
    planet_response = []

    ### WAVE 5
    params = request.args 
    if "name" and "description" and "miles_from_sun" in params:
        name_value = params["name"]
        description_value = params["description"]
        miles_from_sun_value = params["miles_from_sun"]
        planets = Planet.query.filter_by(name=name_value, description=description_value, miles_from_sun=miles_from_sun_value)
    elif "name" in params:
        name_value = params["name"]
        planets = Planet.query.filter_by(name=name_value)
    elif "description" in params:
        description_value = params["description"]
        planets = Planet.query.filter_by(description=description_value)
    elif "miles_from_sun" in params:
        miles_from_sun_value = params["miles_from_sun"]
        planets = Planet.query.filter_by(miles_from_sun=miles_from_sun_value)
    else:
        planets = Planet.query.all()

    for planet in planets:
        planet_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "miles_from_sun": planet.miles_from_sun
        })

    return jsonify(planet_response)

### WAVE 4
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"planet {planet_id} is invalid"}, 400))
    
    planet = Planet.query.get(planet_id)
    if not planet: 
        abort(make_response({"message": f"planet {planet_id} not found"}, 404))

    return planet 

@planets_bp.route('/<planet_id>', methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name, 
        "description": planet.description,
        "miles_from_sun": planet.miles_from_sun,
    }

@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    try: 
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.miles_from_sun = request_body["miles_from_sun"]
    except KeyError:
        return {
            "msg": "name, description, and miles from sun are required"
        }, 400 

    db.session.commit()

    return f"Planet #{planet_id} succesfully updated"

@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return f"Planet #{planet_id} successfully deleted"

### WAVE 2
# @planets_bp.route("", methods=["GET"])
# def get_all_planets():
#     planet_response = []

#     for planet in planets:
#         planet_response.append({
#             "id": planet.id,
#             "name": planet.name,
#             "description": planet.description,
#             "distance_from_sun": planet.distance_from_sun
#         })

#     return jsonify(planet_response)

# @planets_bp.route("/<planet_id>", methods=["GET"])
# def get_planet(planet_id):
#     chosen_planet = None
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         rsp = {"message": f"Invalid planet id {planet_id}"}
#         return jsonify(rsp), 400

#     for planet in planets:
#         if planet_id == planet.id:
#             chosen_planet = planet
#             break
#     if chosen_planet is None:
#         rsp = {"message": f"Could not find planet with id {planet_id}"}
#         return jsonify(rsp), 404      
            
#     rsp = {
#         "id": planet.id,
#         "name": planet.name,
#         "description": planet.description,
#         "distance_from_sun": planet.distance_from_sun
#     }

#     return jsonify(rsp), 200




