import random
import requests

from domain.pokemon import Pokemon
from infraestructure.repositories.pokemon_repository import PokemonRepository
from domain.user import User


class PokemonService:

    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon/"
        self.repository = PokemonRepository()


    def get_random_pokemon_data(self, user, is_shiny):
        """
        Get a random pokemon from the first generation (1 - 151)
        Avoid duplicates when possible
        """

        captured = {p.dex_number for p in user.pokemons}

        available = [i for i in range(1, 152) if i not in captured]

        if not available:
            random_id = random.randint(1, 151)
        else:
            random_id = random.choice(available)
        
        response = requests.get(f"{self.base_url}{random_id}")

        if response.status_code != 200:
            return None

        data = response.json()

        types = [t["type"]["name"] for t in data["types"]]

        sprite = (
            data["sprites"]["front_shiny"]
            if is_shiny
            else data["sprites"]["front_default"]
        )

        return {
            "dex": random_id,
            "name": data["name"],
            "sprite": sprite,
            "type1": types[0],
            "type2": types[1] if len(types) > 1 else None
        }


    def assign_random_pokemon_to_user(self, user_id: int, user_level: int):
        """
        Create and save the pokemon for the user
        """

        user = User.query.get(user_id)

        is_shiny = self.generate_shiny(user)

        pokemon_data = self.get_random_pokemon_data(user, is_shiny)

        if not pokemon_data:
            pokemon_data = {
                "dex": 25,
                "name": "pikachu",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
            }

        rarity = self.generate_rarity(user_level)

        existing_pokemon = self.repository.get_by_user_and_dex(
            user_id,
            pokemon_data["dex"]
        )

        if existing_pokemon:
            return None

        new_pokemon = Pokemon(
            dex_number=pokemon_data["dex"],
            name=pokemon_data["name"],
            sprite_url=pokemon_data["sprite"],
            rarity=rarity,
            is_shiny=is_shiny,
            type1 = pokemon_data["type1"],
            type2 = pokemon_data["type2"],
            user_id=user_id
        )

        self.repository.add(new_pokemon)

        return new_pokemon


    def generate_rarity(self, user_level):

        roll = random.randint(1, 100)

        if user_level < 10:
            if roll <= 85:
                return "normal"
            elif roll <= 98:
                return "rare"
            else:
                return "mythic"

        elif user_level < 25:

            if roll <= 65:
                return "normal"
            elif roll <= 90:
                return "rare"
            elif roll <= 98:
                return "mythic"
            else:
                return "legendary"

        else:

            if roll <= 50:
                return "normal"
            elif roll <= 80:
                return "rare"
            elif roll <= 95:
                return "mythic"
            else:
                return "legendary"


    def generate_shiny(self, user):
        """
        If the user completes the pokedex → shiny hunt mode
        """

        if len(user.pokemons) >= 151:
            return True

        return random.randint(1, 100) == 1