from infraestructure.db import db

class Pokemon(db.Model):
    __tablename__ = "pokemons"

    id = db.Column(db.Integer, primary_key = True)
    dex_number = db.Column(db.Integer)

    name = db.Column(db.String(100), nullable = False)
    sprite_url = db.Column(db.String(300))

    rarity = db.Column(db.String(20), default = "normal")
    is_shiny = db.Column(db.Boolean, default = False)

    type1 = db.Column(db.String(20))
    type2 = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __repr__(self):
        return f"<Pokemon {self.name}>"