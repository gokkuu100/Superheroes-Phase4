from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Routes for getting heroes, hero details, powers, and power details
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 
                  'name': hero.name, 
                  'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        powers = [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description} for hp in hero.hero_powers]
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': powers
        }
        return jsonify(hero_data)
    else:
        response = jsonify({'error': 'Hero not found'})
        response.status_code = 404
        return response

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)

@app.route('/powers/<int:power_id>', methods=['GET', 'PATCH'])
def get_or_update_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        response = jsonify({'error': 'Power not found'})
        response.status_code = 404
        return response
    
    if request.method == 'GET':
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    
    if request.method == 'PATCH':
        data = request.get_json()
        description = data.get('description')
        if description:
            power.description = description
            db.session.commit()
            return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
        else:
            response = jsonify({'errors': ['Invalid data']})
            response.status_code = 400
            return response

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if not hero_id or not power_id or not strength:
        response = jsonify({'errors': ['Invalid data']})
        response.status_code = 400
        return response

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        response = jsonify({'errors': ['Hero or Power not found']})
        response.status_code = 404
        return response

    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    powers = [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description} for hp in hero.hero_powers]
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }
    return jsonify(hero_data)

if __name__ == '__main__':
    app.run(port=5555)
