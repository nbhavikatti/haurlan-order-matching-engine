# Represents one user's holdings in a single market
# A Position tracks how many YES and NO shares the user owns
# as a result of completed trades.
class Position:

    # yes_shares: the number of yes_shares a user owns. Can be negative: short selling YES.
    # no_shares: the number of no_shares a user owns. Not fully implemented due to time constraints. 

    def __init__(self, yes_shares = 0, no_shares = 0):
        
        #if no_shares < 0:
        #    raise ValueError("no_shares cannot be negative")
        
        self.yes_shares = yes_shares
        self.no_shares = no_shares

    def to_dict(self):
        return {
            "yes_shares": self.yes_shares,
            "no_shares": self.no_shares
        }
