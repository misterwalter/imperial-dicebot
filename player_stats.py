"""Record of all rolls by a given player. Player name is not stored in the record as it is the key that the record is looked up by."""
"""Does not currently support tracking generic rolls"""

from collections import defaultdict

class PlayerStats:

    def __init__(self):
        self.score = 0
        self.dice = 0
        self.score_per_side = defaultdict(int)  ## Total value rolled with this particular number of sides
        self.dice_per_side = defaultdict(int)   ## Total dice rolled with this number of sides.


    # Returns a readable record of player info
    def get_report(self, mention : str):
        report = f"{mention} Rolled:"
        sides = list(self.score_per_side.keys())
        sides.sort()
        for side in sides:
            actual_average = 1.0*self.score_per_side[side]/self.dice_per_side[side]
            expected_average = (side + 1)/2.0
            emoji = ":small_red_triangle_down:" if expected_average > actual_average else ":arrow_up_small:"
            report = f"{report}\n{self.dice_per_side[side]} d{side}s\n_Total:_ {self.score_per_side[side]}"
            report = f"{report} Average: {actual_average:.3f} ({expected_average:.1f} expected) {emoji}"
        return report