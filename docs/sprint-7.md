# Sprint 7

## Duration 
2 Days

---

## Sprint Goal

Enchance the trainer profile experience and improve the Pokemon collection system by introducing a full Pokedex view, visual improvements and interaction features while maintaining the existing gamification mechanics and architectural separation.

This sprint focuses on improving user engagement and visual feedback without altering the core business logic implemented in previous sprints.

---

## Selected User Stories

- US-16 - Trainer Profile Page (Enhancement)
- Internal Improvement - Pokedex visualization and interaction

---

## Functional Scope

### Pokedex Collection System

- Display the full Pokedex from generation 1 (1 - 151)
- Captured Pokemon appear with:
    - Sprite
    - Name
    - Rarity label
    - Shiny badge when applicable
- Non-captured Pokemon appear as silhouettes
- Pokedex progress indicators shows completion percentage

### Pokemon Detail Modal

- Clicking on a captured Pokemon opens a modal window
- Modal displays:
    - Pokemon name
    - Sprite
    - Type
    - Height
    - Weight
    - Abilities
- Data is retrieved dynamically from the PokeAPI

### Visual Improvements

- Pokemon cards use type-based gradient backgrounds
- Newly captured Pokemon are highlighted with a visual indicator
- Pokemon types dynamically control card styling
- UI improved to resemble a Pokedex interface

### Interaction Improvements

- Pokemon modal only opens for captured Pokemon
- Silhouette Pokemon cannot trigger modal interactions
- Pokemon details load dynamically using asynchronous API calls

---

## Technical Tasks

- Implement full Pokedex generation logic in ProfileService
- Extend Pokemon model with type information
- Add PokemonRepository for persitance abstraction
- Refactor PokemonService to delegate database operations to repository
- Implement dynamic Pokemon modal using JavaScript
- Integrate PokeAPI data retrieval in the frontend
- Add type-based CSS styling for Pokemon cards
- Implement highlight logic for newly captured Pokemon

---

## Architecture Impact

Sprint 7 reinforces the layered architecture by improving separation of concerns.

Changes introduced:

- PokemonRepository added to the Persitance Layer
- PokemonService refactored to delegate database operations
- ProfileService extended to construct full Pokedex dataset

Architecture remains consistent:

- Flask (Controller Layer)
- Services (Business Logic Layer)
- Repositories (Persistance Layer)
- Domain Models (Domain Layer)

No business logic was introduced in the UI.

---

## Increment Delivered

At the end of Sprint 7, the application:

- Displays a complete Pokedex collection
- Differentials captured and non-captured Pokemon visually
- Shows detailed Pokemon information through an interactive modal
- Highlights newly captured Pokemon
- Uses type-based styling for improved visual feedback
- Maintains clean architecture separation
- Improves user engagement through enhanced gamification