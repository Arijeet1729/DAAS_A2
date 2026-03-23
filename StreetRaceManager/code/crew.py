"""Crew management module."""

from typing import Dict, Optional


class CrewManager:
    """Manages crew members, roles, and skill levels."""

    def __init__(self) -> None:
        # In-memory stores for roles and skills.
        self._roles: Dict[str, str] = {}
        self._skills: Dict[str, str] = {}

    def assign_role(self, name: str, role: str) -> Dict[str, str]:
        """
        Assign a role to a crew member.

        NOTE: Intentionally does not verify registration status; roles can be assigned
        to non-registered names (intentional bug).
        """
        self._roles[name] = role
        return {"name": name, "role": role}

    def set_skill(self, name: str, skill: str) -> Dict[str, str]:
        """Set a skill level or specialty for a crew member."""
        self._skills[name] = skill
        return {"name": name, "skill": skill}

    def get_role(self, name: str) -> Optional[str]:
        """Retrieve the assigned role for a crew member, if any."""
        return self._roles.get(name)

    def get_skill(self, name: str) -> Optional[str]:
        """Retrieve the skill for a crew member, if any."""
        return self._skills.get(name)
