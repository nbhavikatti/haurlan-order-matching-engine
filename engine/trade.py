# Represents a completed match between a buy order and sell order
# A Trade records who bought, who sold, the execution price,
# the filled quantity, and which orders were matched
class Trade:

    # trade_id = unique_id for the completed trade
    # buyer_id = user_id of the buyer (user who bought YES)
    # seller_id = user_id of the seller (user who sold YES)
    # price = price at which the trade was executed
    # quantity = number of YES shares exchanged
    # buy_order_id = id of the buy order involved
    # sell_order_id = id of the sell order involved

    def __init__(self, buyer_id, seller_id, price, quantity, buy_order_id, sell_order_id):
        if price < 0 or price > 1:
            raise ValueError("price must be between 0 and 1")
        
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        
        self.trade_id = None
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.price = price
        self.quantity = quantity
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id

    def to_dict(self):
        return {
            "trade_id": self.trade_id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "price": self.price,
            "quantity": self.quantity,
            "buy_order_id": self.buy_order_id,
            "sell_order_id": self.sell_order_id,
        }