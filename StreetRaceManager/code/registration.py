"""Registration module for StreetRaceManager."""

from typing import Dict, List, Optional


class RegistrationManager:
    """Handles crew member registrations."""

    def __init__(self) -> None:
        # In-memory store for crew members; allows duplicates by design (intentional bug).
        self._members: List[Dict[str, str]] = []

    def register_member(self, name: str, role: str) -> Dict[str, str]:
        """
        Register a crew member.

        NOTE: Duplicate registrations are allowed intentionally; no uniqueness check is performed.
        """
        member = {"name": name, "role": role}
        self._members.append(member)
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
