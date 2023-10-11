from random import choice, sample
from faker import Faker
from app import app
from models import db, Power, Hero, HeroPower

fake = Faker()

def seed_powers():
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]
    for power_data in powers_data:
        power = Power(**power_data)
        db.session.add(power)
    db.session.commit()

def seed_heroes():
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]
    for hero_data in heroes_data:
        hero = Hero(**hero_data)
        db.session.add(hero)
    db.session.commit()

def assign_powers_to_heroes():
    heroes = Hero.query.all()
    powers = Power.query.all()
    strengths = ["Strong", "Weak", "Average"]

    for hero in heroes:
        num_powers = choice(range(1, 4))
        selected_powers = sample(powers, num_powers)
        for power in selected_powers:
            hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=choice(strengths))
            db.session.add(hero_power)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        print("🦸‍♀️ Seeding powers...")
        seed_powers()
        print("🦸‍♀️ Seeding heroes...")
        seed_heroes()
        print("🦸‍♀️ Adding powers to heroes...")
        assign_powers_to_heroes()
        print("🦸‍♀️ Done seeding!")
