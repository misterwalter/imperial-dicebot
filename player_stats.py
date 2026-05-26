"""Record of all rolls by a given player. Player name is not stored in the record as it is the key that the record is looked up by."""
"""Does not currently support tracking generic rolls"""

class PlayerStats:

    def __init__(self):
        self.successes = 0
        self.dice = 0
        self.rolls = 0
    
    # Returns a readable record of player info
    def get_report(self, mention : str):
        accuracy = 0 if self.dice == 0 else 100*self.success/self.dice
        efficiency = 0 if self.rolls == 0 else self.successes/self.rolls
        return """
{mention}'s performance for today:
    {successes} out of {dice} dice ({accuracy}%) on {rolls} rolls.
    You rolled an average of {efficiency} successes per roll.
    """.format(
        mention = mention,
        successes = self.successes,
        dice = self.dice,
        rolls = self.rolls,
        accuracy = accuracy,
        efficiency = efficiency,
    )