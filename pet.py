# pet.py
import random


class VirtualPet:
    """
    Core game logic for the virtual pet.
    Handles attributes, actions, time-based decay, random events, and game-over.
    """

    def __init__(self, name: str = "Virtual Pet"):
        self.name = name
        self.hunger = 50      # 0 = full, 100 = starving
        self.happiness = 70   # 0 = miserable, 100 = very happy
        self.energy = 80      # 0 = exhausted, 100 = full of energy
        self.alive = True
        self.status_message = "Your pet is ready to play!"

    # ---------- helpers ----------
    def _clamp_stats(self) -> None:
        """Keep all stats between 0 and 100."""
        self.hunger = max(0, min(100, self.hunger))
        self.happiness = max(0, min(100, self.happiness))
        self.energy = max(0, min(100, self.energy))

    def _check_game_over(self) -> str | None:
        """Check if the pet has reached a game-over condition."""
        if self.hunger >= 100:
            self.alive = False
            return f"{self.name} got too hungry and collapsed... Game over."
        if self.energy <= 0:
            self.alive = False
            return f"{self.name} ran out of energy and fell asleep forever... Game over."
        if self.happiness <= 0:
            self.alive = False
            return f"{self.name} became too unhappy and ran away... Game over."
        return None

    # ---------- player actions ----------
    def feed(self) -> str:
        if not self.alive:
            return "The pet cannot eat anymore. Game over."

        self.hunger -= 20
        self.energy += 5
        self.happiness += 5
        self._clamp_stats()
        msg = f"You fed {self.name}. Yum! Hunger decreased."

        game_over = self._check_game_over()
        return game_over or msg

    def play(self) -> str:
        if not self.alive:
            return "The pet cannot play anymore. Game over."

        self.happiness += 15
        self.energy -= 15
        self.hunger += 10
        self._clamp_stats()
        msg = f"{self.name} played happily! Happiness increased."

        game_over = self._check_game_over()
        return game_over or msg

    def rest(self) -> str:
        if not self.alive:
            return "The pet cannot rest anymore. Game over."

        self.energy += 25
        self.hunger += 10
        self._clamp_stats()
        msg = f"{self.name} took a nap. Energy restored."

        game_over = self._check_game_over()
        return game_over or msg

    # ---------- time-based changes ----------
    def tick(self) -> str | None:
        """
        Natural decay that happens every few seconds.
        Called from the GUI using Tkinter's .after().
        """
        if not self.alive:
            return None

        # Natural changes
        self.hunger += 3
        self.energy -= 2
        self.happiness -= 1
        self._clamp_stats()

        # Check for random events
        event_msg = self._random_event()

        # Game-over check
        game_over = self._check_game_over()
        if game_over:
            return game_over

        return event_msg

    # ---------- random events ----------
    def _random_event(self) -> str | None:
        """
        With some probability, trigger a random event that affects stats.
        """
        if random.random() > 0.25:  # 25% chance each tick
            return None

        event = random.choice(
            [
                "toy",
                "snack",
                "sick",
                "zoomies",
                "bored",
            ]
        )

        if event == "toy":
            self.happiness += 10
            self._clamp_stats()
            return f"{self.name} found a new toy! Happiness increased."
        elif event == "snack":
            self.hunger -= 10
            self._clamp_stats()
            return f"{self.name} found a snack on the floor. Hunger decreased."
        elif event == "sick":
            self.energy -= 10
            self.happiness -= 5
            self._clamp_stats()
            return f"Oh no! {self.name} feels a bit sick. Energy and happiness decreased."
        elif event == "zoomies":
            self.energy -= 10
            self.happiness += 10
            self.hunger += 5
            self._clamp_stats()
            return f"{self.name} has the zoomies! Very excited but tired and hungry."
        elif event == "bored":
            self.happiness -= 10
            self._clamp_stats()
            return f"{self.name} is getting bored... Happiness decreased."

        return None

    # ---------- data for GUI ----------
    def get_stats(self) -> dict:
        return {
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
        }
import random


class VirtualPet:
    """
    Core game logic for the virtual pet.
    Handles attributes, actions, time-based decay, random events, and game-over.
    """

    def __init__(self, name: str = "Virtual Pet"):
        self.name = name
        self.hunger = 50      # 0 = full, 100 = starving
        self.happiness = 70   # 0 = miserable, 100 = very happy
        self.energy = 80      # 0 = exhausted, 100 = full of energy
        self.alive = True
        self.status_message = "Your pet is ready to play!"

    # ---------- helpers ----------
    def _clamp_stats(self) -> None:
        """Keep all stats between 0 and 100."""
        self.hunger = max(0, min(100, self.hunger))
        self.happiness = max(0, min(100, self.happiness))
        self.energy = max(0, min(100, self.energy))

    def _check_game_over(self) -> str | None:
        """Check if the pet has reached a game-over condition."""
        if self.hunger >= 100:
            self.alive = False
            return f"{self.name} got too hungry and collapsed... Game over."
        if self.energy <= 0:
            self.alive = False
            return f"{self.name} ran out of energy and fell asleep forever... Game over."
        if self.happiness <= 0:
            self.alive = False
            return f"{self.name} became too unhappy and ran away... Game over."
        return None

    # ---------- player actions ----------
    def feed(self) -> str:
        if not self.alive:
            return "The pet cannot eat anymore. Game over."

        self.hunger -= 20
        self.energy += 5
        self.happiness += 5
        self._clamp_stats()
        msg = f"You fed {self.name}. Yum! Hunger decreased."

        game_over = self._check_game_over()
        return game_over or msg

    def play(self) -> str:
        if not self.alive:
            return "The pet cannot play anymore. Game over."

        self.happiness += 15
        self.energy -= 15
        self.hunger += 10
        self._clamp_stats()
        msg = f"{self.name} played happily! Happiness increased."

        game_over = self._check_game_over()
        return game_over or msg

    def rest(self) -> str:
        if not self.alive:
            return "The pet cannot rest anymore. Game over."

        self.energy += 25
        self.hunger += 10
        self._clamp_stats()
        msg = f"{self.name} took a nap. Energy restored."

        game_over = self._check_game_over()
        return game_over or msg

    # ---------- time-based changes ----------
    def tick(self) -> str | None:
        """
        Natural decay that happens every few seconds.
        Called from the GUI using Tkinter's .after().
        """
        if not self.alive:
            return None

        # Natural changes
        self.hunger += 3
        self.energy -= 2
        self.happiness -= 1
        self._clamp_stats()

        # Check for random events
        event_msg = self._random_event()

        # Game-over check
        game_over = self._check_game_over()
        if game_over:
            return game_over

        return event_msg

    # ---------- random events ----------
    def _random_event(self) -> str | None:
        """
        With some probability, trigger a random event that affects stats.
        """
        if random.random() > 0.25:  # 25% chance each tick
            return None

        event = random.choice(
            [
                "toy",
                "snack",
                "sick",
                "zoomies",
                "bored",
            ]
        )

        if event == "toy":
            self.happiness += 10
            self._clamp_stats()
            return f"{self.name} found a new toy! Happiness increased."
        elif event == "snack":
            self.hunger -= 10
            self._clamp_stats()
            return f"{self.name} found a snack on the floor. Hunger decreased."
        elif event == "sick":
            self.energy -= 10
            self.happiness -= 5
            self._clamp_stats()
            return f"Oh no! {self.name} feels a bit sick. Energy and happiness decreased."
        elif event == "zoomies":
            self.energy -= 10
            self.happiness += 10
            self.hunger += 5
            self._clamp_stats()
            return f"{self.name} has the zoomies! Very excited but tired and hungry."
        elif event == "bored":
            self.happiness -= 10
            self._clamp_stats()
            return f"{self.name} is getting bored... Happiness decreased."

        return None

    # ---------- data for GUI ----------
    def get_stats(self) -> dict:
        return {
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
        }
