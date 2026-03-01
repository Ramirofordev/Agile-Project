import random
import requests 
from domain.pokemon import Pokemon
from infraestructure.db import db

class PokemonService:

    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon/"

    def get_random_pokemon_data(self):
        """
        Get a random pokemon from the first generation (1 - 151)
        """

        random_id = random.randint(1, 151)

        response = requests.get(f"{self.base_url}{random_id}")

        if response.status_code != 200:
            return None
        
        data = response.json()

        return {
            "name": data["name"],
            "sprite": data["sprites"]["front_default"]
        }

    def assign_random_pokemon_to_user(self, user_id: int):
        """
        Create and safe the pokemon for the user
        """

        pokemon_data = self.get_random_pokemon_data()

        if not pokemon_data:
            pokemon_data = {
                "name": "pikachu",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
            }
        
        new_pokemon = Pokemon(
            name = pokemon_data["name"],
            sprite_url = pokemon_data["sprite"],
            user_id = user_id
        )

        db.session.add(new_pokemon)
        db.session.commit()

        return new_pokemon