from fastapi import FastAPI
from pydantic import BaseModel

from engine.market import Market
from engine.order import Order

class CreateMarketRequest(BaseModel):
    question: str

class SubmitOrderRequest(BaseModel):
    user_id: str
    side: str
    price: float
    quantity: int

# maps market_ids -> Market objects
markets = {}
next_market_id = 0

app = FastAPI()

# GET /
@app.get("/")
def health_check():
    return {"message": "Haurlan binary outcome market API is running"}

# POST /markets
@app.post("/markets")
def create_market(request: CreateMarketRequest):
    global next_market_id

    market_id = next_market_id
    next_market_id += 1

    market = Market(market_id, request.question)
    markets[market_id] = market

    return {
        "market_id": market_id,
        "question": market.question,
        "status": market.status,
        "outcome": market.outcome
    }

# POST /markets/{market_id}/orders
@app.post("/markets/{market_id}/orders")
def submit_order(market_id: int, request: SubmitOrderRequest):
    if market_id not in markets:
        raise ValueError("market_id must be valid")

    market = markets[market_id]

    order = Order(
        request.user_id,
        request.side,
        request.price,
        request.quantity
    )

    trades = market.submit_order(order)

    return {
        "order": order.to_dict(),
        "trades": [trade.to_dict() for trade in trades],
        "order_book": market.order_book.get_snapshot()
    }

# GET /markets/{market_id}/orderbook
@app.get("/markets/{market_id}/orderbook")
def get_order_book(market_id: int):
    if market_id not in markets:
        raise ValueError("market_id must be valid")

    market = markets[market_id]
    return market.order_book.get_snapshot()

# GET /markets/{market_id}/trades
@app.get("/markets/{market_id}/trades")
def get_trades(market_id: int):
    if market_id not in markets:
        raise ValueError("market_id must be valid")

    market = markets[market_id]
    return [trade.to_dict() for trade in market.trades]

# GET /markets/{market_id}/positions
@app.get("/markets/{market_id}/positions")
def get_positions(market_id: int):
    if market_id not in markets:
        raise ValueError("market_id must be valid")

    market = markets[market_id]
    return {
        user_id: position.to_dict()
        for user_id, position in market.positions.items()
    }

# DELETE /markets/{market_id}/orders/{order_id}
@app.delete("/markets/{market_id}/orders/{order_id}")
def cancel_order(market_id: int, order_id: int, side: str):
    if market_id not in markets:
        raise ValueError("market_id must be valid")

    market = markets[market_id]
    market.cancel_order(order_id, side)

    return {
        "message": "order cancelled",
        "order_book": market.order_book.get_snapshot()
    }




