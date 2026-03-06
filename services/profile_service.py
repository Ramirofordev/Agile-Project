class ProfileService:

    TOTAL_POKEMON = 151

    # POKEDEX BUILD

    def build_pokedex(self, user): 
        """
        Builds the full pokedex (1-151) mixing captured
        and non-captured pokemon
        """

        captured_by_dex = {p.dex_number: p for p in user.pokemons}

        pokedex = []

        for dex in range(1, self.TOTAL_POKEMON + 1):

            if dex in captured_by_dex:

                p = captured_by_dex[dex]

                pokedex.append({
                    "dex": dex,
                    "captured": True,
                    "name": p.name,
                    "sprite_url": p.sprite_url,
                    "rarity": p.rarity,
                    "is_shiny": p.is_shiny,
                    "type1": p.type1,
                    "type2": p.type2
                })

            else:

                pokedex.append({
                    "dex": dex,
                    "captured": False,
                    "type1": None,
                    "type2": None
                })

        return pokedex
    

    # PROFILE STATS

    def get_profile_stats(self, user):
        """
        Returns statistics for the trainer card
        """

        captured = len(user.pokemons)

        percent = round((captured / self.TOTAL_POKEMON) * 100)

        shinies = sum(1 for p in user.pokemons if p.is_shiny)

        legendary = sum(1 for p in user.pokemons if p.rarity == "legendary")

        return {
            "captured": captured,
            "percent": percent,
            "shinies": shinies,
            "legendary": legendary
        }
    
    # Achievements

    def get_achievements(self, stats):
        """
        Generates achievements dynamically based on stats
        """

        achievements = []

        captured = stats["captured"]
        shinies = stats["shinies"]
        legendary = stats["legendary"]
        percent = stats["percent"]

        if captured >= 1:
            achievements.append({
                "name": "First Catch",
                "icon": "🎖️"
            })

        if captured >= 30:
            achievements.append({
                "name": "Collector",
                "icon": "🎒"
            })

        if captured >= 60:
            achievements.append({
                "name": "Master Collector",
                "icon": "🏆"
            })

        if shinies >= 1:
            achievements.append({
                "name": "Shiny Hunter",
                "icon": "✨"
            })
        
        if legendary >= 1:
            achievements.append({
                "name": "Legendary Hunter",
                "icon": "⭐"
            })

        if percent >= 10:
            achievements.append({
                "name": "Pokedex Beginner",
                "icon": "📖"
            })
        
        return achievements