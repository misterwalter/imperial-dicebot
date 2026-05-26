"""Record of all rolls by a given player. Player name is not stored in the record as it is the key that the record is looked up by."""
"""Does not currently support tracking generic rolls"""

from collections import defaultdict

class PlayerStats:

    def __init__(self):
        self.successes = 0
        self.dice = 0
        self.rolls = 0
        self.score_per_side = defaultdict(int)  ## Total value rolled with this particular number of sides
        self.dice_per_side = defaultdict(int)   ## Total dice rolled with this number of sides.

    # Returns a readable record of player info
    def get_report(self, mention : str):
        accuracy = 0 if self.dice == 0 else 100*self.successes/self.dice
        efficiency = 0 if self.rolls == 0 else self.successes/self.rolls
        return f"""
{mention}'s performance for today:
    {self.successes} out of {self.dice} dice ({accuracy}%) on {self.rolls} rolls.
    You rolled an average of {efficiency} successes per roll.
    {self.score_per_side}
    {self.dice_per_side}
    """