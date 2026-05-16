from urllib.parse import urlparse


class ProfileService:

    TOTAL_POKEMON = 151
    BLOCKED_WORDS = {
        "fuck",
        "shit",
        "bitch",
        "asshole",
        "puta",
        "puto",
        "mierda",
        "pendejo",
        "pendeja",
        "cabron",
        "cabrón",
        "verga",
        "culo"
    }

    ALLOWED_AVATAR_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    ALLOWED_AVATAR_MIMES = {"image/png", "image/jpeg", "image/webp"}
    MAX_AVATAR_BYTES = 2 * 1024 * 1024

    def contains_blocked_language(self, value):
        normalized = (value or "").lower()
        return any(word in normalized for word in self.BLOCKED_WORDS)

    def validate_profile_text(self, display_name, bio, focus_goal, resource_label):
        fields = [display_name, bio, focus_goal, resource_label]

        if any(self.contains_blocked_language(field) for field in fields):
            raise ValueError("Profile text contains blocked language")

        if display_name and len(display_name.strip()) > 100:
            raise ValueError("Display name is too long")

        if bio and len(bio.strip()) > 500:
            raise ValueError("Bio is too long")

        if focus_goal and len(focus_goal.strip()) > 200:
            raise ValueError("Focus goal is too long")

        if resource_label and len(resource_label.strip()) > 80:
            raise ValueError("Resource label is too long")

    def validate_resource_url(self, resource_url):
        if not resource_url:
            return

        parsed = urlparse(resource_url.strip())

        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Resource URL must be a valid http or https link")

        if len(resource_url.strip()) > 300:
            raise ValueError("Resource URL is too long")

    def validate_avatar(self, avatar_file):
        if not avatar_file or not avatar_file.filename:
            return

        extension = avatar_file.filename.rsplit(".", 1)[-1].lower()

        if extension not in self.ALLOWED_AVATAR_EXTENSIONS:
            raise ValueError("Avatar must be a PNG, JPG, JPEG, or WEBP image")

        if avatar_file.mimetype not in self.ALLOWED_AVATAR_MIMES:
            raise ValueError("Avatar file type is not allowed")

        avatar_file.stream.seek(0, 2)
        size = avatar_file.stream.tell()
        avatar_file.stream.seek(0)

        if size > self.MAX_AVATAR_BYTES:
            raise ValueError("Avatar must be 2 MB or smaller")

    def update_profile(self, user, display_name, bio, focus_goal, resource_label, resource_url):
        self.validate_profile_text(display_name, bio, focus_goal, resource_label)
        self.validate_resource_url(resource_url)

        user.display_name = display_name.strip() if display_name else None
        user.bio = bio.strip() if bio else None
        user.focus_goal = focus_goal.strip() if focus_goal else None
        user.resource_label = resource_label.strip() if resource_label else None
        user.resource_url = resource_url.strip() if resource_url else None

        return user

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
