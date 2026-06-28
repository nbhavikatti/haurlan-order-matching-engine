from engine.trade import Trade
# there is one OrderBook per Market
# store active unmatched orders and eventually match/cancel them
# Maintains buy/sell orders in price-time priority order, and supports
# adding, cancelling, and viewing orders
class OrderBook:

    # buy_orders = active unmatched orders trying to buy YES
    # sell_orders = active unmatched orders trying to sell YES

    def __init__(self, buy_orders=None, sell_orders=None):
        if buy_orders is None:
            self.buy_orders = []
        else:
            self.buy_orders = buy_orders
        if sell_orders is None:
            self.sell_orders = []
        else:
            self.sell_orders = sell_orders
        self.next_order_id = 0 

    # look at order.side. If side is "BUY", append to buy_orders
    # If side is "SELL", append to sell_orders
    # If side is neither, reject with ValueError
    # returns a list of trades created
    def add_order(self, order):

        trades = []

        if order.side == "BUY" or order.side == "SELL":
            order.order_id = self.next_order_id
            self.next_order_id += 1
            if order.side == "BUY":
                # try matching against sell orders
                # if quantity remains, add to buy_orders
                while (order.quantity > 0 and len(self.sell_orders) > 0 and order.price >= self.sell_orders[0].price):
                    resting_sell = self.sell_orders[0]
                    trade_quantity = min(order.quantity, resting_sell.quantity)
                    trade_price = resting_sell.price
                    t = Trade(order.user_id, resting_sell.user_id, trade_price, trade_quantity, order.order_id, resting_sell.order_id)
                    trades.append(t)
                    order.quantity -= trade_quantity
                    resting_sell.quantity -= trade_quantity

                    if resting_sell.quantity == 0:
                        del self.sell_orders[0]

                if order.quantity > 0:
                    self.buy_orders.append(order)
                    self.buy_orders.sort(key = lambda order : (-order.price, order.order_id))
            else:
                # try matching against buy orders
                # if quantity remains, add to sell_orders
                while (order.quantity > 0 and len(self.buy_orders) > 0 and order.price <= self.buy_orders[0].price):
                    resting_buy = self.buy_orders[0]
                    trade_quantity = min(order.quantity, resting_buy.quantity)
                    trade_price = resting_buy.price
                    t = Trade(resting_buy.user_id, order.user_id, trade_price, trade_quantity, resting_buy.order_id, order.order_id)
                    trades.append(t)
                    order.quantity -= trade_quantity
                    resting_buy.quantity -= trade_quantity

                    if resting_buy.quantity == 0:
                        del self.buy_orders[0]

                if order.quantity > 0:
                    self.sell_orders.append(order)
                    self.sell_orders.sort(key = lambda order : (order.price, order.order_id))
        else:
            raise ValueError("order side must be BUY or SELL")
        
        return trades

    # cancel_order from BUY list or SELL list depending on order_id. 
    # raise ValueError if order_id or side is invalid
    def cancel_order(self, order_id, side):
        if side == "BUY":
            for i in range(len(self.buy_orders)):
                if self.buy_orders[i].order_id == order_id:
                    del self.buy_orders[i]
                    return
            raise ValueError("order id must be valid")
        elif side == "SELL":
            for i in range(len(self.sell_orders)):
                if self.sell_orders[i].order_id == order_id:
                    del self.sell_orders[i]
                    return
            raise ValueError("order id must be valid")
        else:
            raise ValueError("order side must be BUY or SELL")

    def get_snapshot(self):
        return {
            "buy_orders": [order.to_dict() for order in self.buy_orders],
            "sell_orders": [order.to_dict() for order in self.sell_orders]
        }


        