"""Mission planning module."""

from typing import Dict, List


class MissionPlanner:
    """Manages mission creation and assignments."""

    def __init__(self) -> None:
        self._missions: Dict[str, Dict[str, List[str]]] = {}

    def create_mission(self, mission_id: str, required_roles: List[str]) -> Dict[str, List[str]]:
        """Create a new mission with the required roles."""
        self._missions[mission_id] = {"required_roles": required_roles, "assignees": []}
        return self._missions[mission_id]

    def assign_mission(self, mission_id: str, name: str, role: str) -> Dict[str, str]:
        """
        Assign a crew member to a mission.

        BUG: Does not validate if the role is in required_roles (intentional).
        """
        if mission_id not in self._missions:
            # Auto-create with no requirements if missing
            self.create_mission(mission_id, [])

        assignment = {"name": name, "role": role}
        self._missions[mission_id]["assignees"].append(assignment)
        return assignment

    def list_assignees(self, mission_id: str) -> List[Dict[str, str]]:
        """List all assignees for the given mission."""
        return list(self._missions.get(mission_id, {}).get("assignees", []))
