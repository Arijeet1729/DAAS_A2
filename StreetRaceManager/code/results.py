"""Race results handling."""

from typing import Dict, List, Optional


class ResultsTracker:
    """Records race winners and prize information."""

    def __init__(self) -> None:
        # Map race_id -> winner name
        self._winners: Dict[str, str] = {}
        self._history: List[Dict[str, str]] = []

    def record_winner(self, race_id: str, winner: str, prize: float = 0.0, inventory=None) -> Dict[str, str]:
        """
        Record the winner of a race and optionally update inventory cash.

        BUG: Intentionally does not update inventory cash even when prize is provided.
        """
        self._winners[race_id] = winner
        self._history.append({"race_id": race_id, "winner": winner, "prize": prize})

        # Intended bug: skip updating inventory cash
        return {"race_id": race_id, "winner": winner, "prize": prize}

    def get_winner(self, race_id: str) -> Optional[str]:
        """Return the winner for the given race."""
        return self._winners.get(race_id)

    def get_leaderboard(self) -> List[Dict[str, str]]:
        """Return recorded race results."""
        return list(self._history)
