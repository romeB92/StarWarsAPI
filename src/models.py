from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

favorite_characters = db.Table(
    "favorite_characters",

    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("character_id", db.ForeignKey("characters.id")),
)

favorite_planets = db.Table(
    "favorite_planets",
   
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("planet_id", db.ForeignKey("planets.id")),
)
favorite_starships = db.Table(
    "favorite_starships",

    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("starship_id", db.ForeignKey("starships.id")),
)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String())

    favorite_characters = db.relationship('Characters',secondary=favorite_characters)
    favorite_planets = db.relationship('Planets',secondary=favorite_planets)
    favorite_starships = db.relationship('Starships',secondary=favorite_starships)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "favorite_characters": list(map(lambda x: x.serialize(), self.favorite_characters)),
            "favorite_planets": list(map(lambda x: x.serialize(), self.favorite_planets)),
            "favorite_starships": list(map(lambda x: x.serialize(), self.favorite_starships))
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(250), nullable=False)
    homeworld = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld": self.homeworld,
            "birth_year": self.birth_year,
            "gender": self.gender,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)


    name = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "gravity": self.gravity,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }
    
class Starships(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    model = db.Column(db.String(250), nullable=False)
    starship_class = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    length = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Starship %r>' % self.model

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacturer": self.manufacturer,
            "length": self.length,
            # do not serialize the password, its a security breach
        }