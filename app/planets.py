from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, distance_from_sun):
        self.id = id
        self.name = name
        self.description = description
        self.distance_from_sun = distance_from_sun


# list of planets
planets = [
    Planet(1, "Earth", "A planet were humans live", 92.96),
    Planet(2, "Mercury", "Smallest planet in the solar system", 30.325),
    Planet(3, "Venus", "It's named after Roman goddess of love and beauty", 67.24)
    
]

#Blueprint

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    planet_response = []

    for planet in planets:
        planet_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "distance_from_sun": planet.distance_from_sun
        })

    return jsonify(planet_response)

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_planet(planet_id):
    chosen_planet = None
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"message": f"Invalid planet id {planet_id}"}
        return jsonify(rsp), 400

    for planet in planets:
        if planet_id == planet.id:
            chosen_planet = planet
            break
    if chosen_planet is None:
        rsp = {"message": f"Could not find planet with id {planet_id}"}
        return jsonify(rsp), 404      
            
    rsp = {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance_from_sun": planet.distance_from_sun
    }

    return jsonify(rsp), 200

        

            
            




