"""Ranking calculation module."""

from typing import Dict, List, Tuple


class RankingCalculator:
    """Calculates and provides rankings for races and missions."""

    def __init__(self) -> None:
        self.rankings: Dict[str, int] = {}

    def record_win(self, driver_name: str) -> int:
        """Record a win for a driver."""
        self.rankings[driver_name] = self.rankings.get(driver_name, 0) + 1
        return self.rankings[driver_name]

    def get_rankings(self) -> List[Tuple[str, int]]:
        """
        Return rankings sorted by wins.
        """
        return sorted(self.rankings.items(), key=lambda item: (-item[1], item[0]))

    def get_wins(self, driver_name: str) -> int:
        """Return total wins for the driver (0 if absent)."""
        return self.rankings.get(driver_name, 0)
