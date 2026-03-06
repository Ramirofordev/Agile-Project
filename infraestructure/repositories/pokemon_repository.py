from infraestructure.db import db
from domain.pokemon import Pokemon

class PokemonRepository:

    def add(self, pokemon: Pokemon):
        db.session.add(pokemon)
        db.session.commit()

    def get_user_pokemon(self, user_id):
        return Pokemon.query.filter_by(user_id = user_id).all()
    
    def get_by_user_and_dex(self, user_id, dex_number):
        return Pokemon.query.filter_by(user_id = user_id,
                                       dex_number = dex_number).first()