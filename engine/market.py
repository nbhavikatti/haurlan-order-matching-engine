from engine.order_book import OrderBook
from engine.position import Position

# Defines a single binary prediction market
# A Market owns the market's metadata, lifecycle state (open, closed, resolved), 
# active order book, completed trades, and user positions

class Market:

    # market_id = unique id for this market
    # question = the actual event with a binary outcome
    # status = "open" (trades can happen), "closed" (no trades, final result not known), or "resolved" (finished)
    # outcome = None at first, later can only be "YES" or "NO"
    # order_book = the active unmatched orders
    # trades = list of completed trades
    # positions = maps user_id -> Position

    def __init__(self, market_id, question, status="open", outcome=None, order_book = None, trades = None, positions = None):
        self.market_id = market_id
        self.question = question
        self.status = status
        self.outcome = outcome
        if order_book is None:
            self.order_book = OrderBook()
        else:
            self.order_book = order_book
        if trades is None:
            self.trades = []
        else:
            self.trades = trades
        if positions is None:
            self.positions = {}
        else:
            self.positions = positions
        self.next_trade_id = 0

    # only True if status is open
    def can_trade(self):
        return self.status == "open"

    # the market is now closed
    def close(self):
        self.status = "closed"

    # market is resolved, a specific outcome has occurred
    def resolve(self, outcome):
        # reject outcome if it is not either "YES" or "NO"
        if outcome != "YES" and outcome != "NO":
            raise ValueError("Outcome must be YES or NO")
        # we are sure outcome is "YES" or "NO" so assign status and outcome vars
        self.status = "resolved"
        self.outcome = outcome

    # reject if market is not open, otherwise send order to order_book
    def submit_order(self, order):
        if not self.can_trade():
            raise ValueError("Market is not open")
        
        # otherwise send order to order_book
        trades = self.order_book.add_order(order)
        for t in trades:
            self.record_trade(t)
        return trades

    # reject if market is not open, otherwise cancel from order_book
    def cancel_order(self, order_id, side):
        if not self.can_trade():
            raise ValueError("Market is not open")
        
        self.order_book.cancel_order(order_id, side)

    # adds trade to self.trades and updates positions
    def record_trade(self, trade):
        trade.trade_id = self.next_trade_id
        self.next_trade_id += 1
        self.trades.append(trade)
        if trade.buyer_id in self.positions:
            self.positions[trade.buyer_id].yes_shares += trade.quantity
        else:
            self.positions[trade.buyer_id] = Position(trade.quantity)
        if trade.seller_id in self.positions:
            self.positions[trade.seller_id].yes_shares -= trade.quantity
        else:
            self.positions[trade.seller_id] = Position(-trade.quantity)
            





