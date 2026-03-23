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
        """
        if mission_id not in self._missions:
            # Auto-create with no requirements if missing
            self.create_mission(mission_id, [])

        required_roles = self._missions[mission_id]["required_roles"]
        if required_roles and role not in required_roles:
            raise ValueError(f"Role '{role}' not permitted; requires one of {required_roles}")

        assignment = {"name": name, "role": role}
        self._missions[mission_id]["assignees"].append(assignment)
        return assignment

    def list_assignees(self, mission_id: str) -> List[Dict[str, str]]:
        """List all assignees for the given mission."""
        return list(self._missions.get(mission_id, {}).get("assignees", []))
