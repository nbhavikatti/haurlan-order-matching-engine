# Represents a single limit order in a market
# An Order records who placed it, whether they want to buy or sell YES,
# the limit price, quantity, and assigned order ID
class Order:
    
    # order_id  = assigned by OrderBook when added
    # user_id = who placed the order
    # side = "BUY" or "SELL"
    # price = price for YES shares
    # quantity = number of YES shares

    def __init__(self, user_id, side, price, quantity):
        if side not in ["BUY", "SELL"]:
            raise ValueError("side must be BUY or SELL")
        
        if price < 0 or price > 1:
            raise ValueError("price must be between 0 and 1")
        
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        
        self.order_id = None
        self.user_id = user_id
        self.side = side
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "side": self.side,
            "price": self.price,
            "quantity": self.quantity
        }
