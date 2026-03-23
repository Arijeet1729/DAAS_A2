"""Registration module for StreetRaceManager."""

from typing import Dict, List, Optional

REGISTERED_NAMES: set[str] = set()


class RegistrationManager:
    """Handles crew member registrations."""

    def __init__(self) -> None:
        # In-memory store for crew members.
        self._members: List[Dict[str, str]] = []

    def register_member(self, name: str, role: str) -> Dict[str, str]:
        """
        Register a crew member.
        """
        if name in REGISTERED_NAMES:
            raise ValueError(f"Member '{name}' already registered")

        member = {"name": name, "role": role}
        self._members.append(member)
        REGISTERED_NAMES.add(name)
        return member

    def get_member(self, name: str) -> Optional[Dict[str, str]]:
        """
        Fetch a crew member by name.

        Returns the first matching member or None if not found.
        """
        for member in self._members:
            if member["name"] == name:
                return member
        return None

    def list_members(self) -> List[Dict[str, str]]:
        """Return all registered crew members (may include duplicates)."""
        return list(self._members)

    def is_registered(self, name: str) -> bool:
        """Check if a name is registered."""
        return name in REGISTERED_NAMES
