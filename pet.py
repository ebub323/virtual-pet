import random


class VirtualPet:


    def __init__(self, name="Virtual Pet"):
        # Starting stats for the pet
        self.name = name
        self.hunger = 50        # 0 = full, 100 = starving
        self.happiness = 70     # 0 = sad, 100 = very happy
        self.energy = 80        # 0 = exhausted, 100 = energized
        self.alive = True       # If False = no more actions allowed

    # keep all attributes within 0–100
    def _clamp_stats(self):
        self.hunger = max(0, min(100, self.hunger))
        self.happiness = max(0, min(100, self.happiness))
        self.energy = max(0, min(100, self.energy))

    # check if any stat causes game over

    def _check_game_over(self):
        if self.hunger >= 100:
            self.alive = False
            return f"{self.name} starved... Game Over."
        if self.energy <= 0:
            self.alive = False
            return f"{self.name} collapsed from exhaustion... Game Over."
        if self.happiness <= 0:
            self.alive = False
            return f"{self.name} became too unhappy and ran away... Game Over."

        return None  # No game-over yet

    # USER ACTIONS

    def feed(self):
        """User feeds the pet = hunger decreases, happiness increases."""
        if not self.alive:
            return "Your pet cannot eat anymore. It is already gone."

        self.hunger -= 20
        self.energy += 5
        self.happiness += 5
        self._clamp_stats()

        msg = f"You fed {self.name}. Hunger decreased!"
        return self._check_game_over() or msg

    def play(self):
        """User plays with the pet = happiness increases but energy drops."""
        if not self.alive:
            return "Your pet cannot play anymore. It is already gone."

        self.happiness += 15
        self.energy -= 15
        self.hunger += 10
        self._clamp_stats()

        msg = f"{self.name} played happily!"
        return self._check_game_over() or msg

    def rest(self):
        """Pet rests = energy increases, hunger slightly increases."""
        if not self.alive:
            return "Your pet cannot rest anymore. It is already gone."

        self.energy += 25
        self.hunger += 10
        self._clamp_stats()

        msg = f"{self.name} took a nap. Energy restored!"
        return self._check_game_over() or msg

    
    # AUTOMATIC DECAY EVERY FEW SECONDS
    
    def tick(self):
        """
        This runs automatically from the GUI every X seconds.
        - Hunger increases gradually
        - Energy decreases gradually
        - Happiness decreases slightly
        Then:
        - A random event may occur
        - Game-over is checked
        """
        if not self.alive:
            return None  # No updates after death

        # Natural stat decay
        self.hunger += 3
        self.energy -= 2
        self.happiness -= 1
        self._clamp_stats()

        # Possibly trigger a random event
        event_msg = self._random_event()

        # Check game-over condition
        game_over_msg = self._check_game_over()
        if game_over_msg:
            return game_over_msg

        return event_msg  # May be None

    # RANDOM EVENTS (25% chance each tick)
    
    def _random_event(self):
        if random.random() > 0.25:
            return None  # 75% of the time = no event

        event = random.choice(["toy", "snack", "sick", "zoomies", "bored"])

        if event == "toy":
            self.happiness += 10
            self._clamp_stats()
            return f"{self.name} found a new toy! Happiness increased."

        if event == "snack":
            self.hunger -= 10
            self._clamp_stats()
            return f"{self.name} found a snack! Hunger decreased."

        if event == "sick":
            self.energy -= 10
            self.happiness -= 5
            self._clamp_stats()
            return f"Oh no! {self.name} got sick. Energy and happiness dropped."

        if event == "zoomies":
            self.energy -= 10
            self.happiness += 10
            self.hunger += 5
            self._clamp_stats()
            return f"{self.name} had the zoomies! Mixed stat changes."

        if event == "bored":
            self.happiness -= 10
            self._clamp_stats()
            return f"{self.name} is bored... Happiness decreased."

        return None

    # RETURN STATS FOR THE GUI

    def get_stats(self):
        """The GUI uses this to update progress bars."""
        return {
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy
        }
