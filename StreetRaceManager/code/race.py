"""Race orchestration module."""

from typing import Dict, List

from code import registration

class RaceController:
    """Controls race scheduling and driver assignments."""

    def __init__(self) -> None:
        # Map race_id -> list of participants (name, role).
        self._races: Dict[str, List[Dict[str, str]]] = {}

    def create_race(self, race_id: str) -> Dict[str, List[Dict[str, str]]]:
        """Create a new race with the given identifier."""
        self._races[race_id] = []
        return {race_id: self._races[race_id]}

    def assign_driver(self, race_id: str, name: str, role: str) -> Dict[str, str]:
        """
        Assign a participant to a race.
        """
        if race_id not in self._races:
            # Auto-create race if it does not exist (lenient behavior).
            self.create_race(race_id)

        if name not in registration.REGISTERED_NAMES:
            raise ValueError(f"Member '{name}' is not registered")
        if role.lower() != "driver":
            raise ValueError("Only drivers may enter a race")

        participant = {"name": name, "role": role}
        self._races[race_id].append(participant)
        return participant

    def list_participants(self, race_id: str) -> List[Dict[str, str]]:
        """List participants for a given race."""
        return list(self._races.get(race_id, []))
