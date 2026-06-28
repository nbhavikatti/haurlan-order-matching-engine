# Haurlan Toy Order Matching Engine

A toy REST API for a binary prediction market order-matching engine.

## What it does

- Create binary outcome markets
- Submit BUY/SELL YES limit orders
- Match orders by price-time priority
- Support partial fills
- Cancel resting orders
- Return order book snapshots
- Return trades and user positions

## How to run

pip install -r requirements.txt

uvicorn main:app --reload

Then open:

http://127.0.0.1:8000/docs

## Main endpoints

POST /markets
POST /markets/{market_id}/orders
DELETE /markets/{market_id}/orders/{order_id}
GET /markets/{market_id}/orderbook
GET /markets/{market_id}/trades
GET /markets/{market_id}/positions

## Design

The API layer lives in main.py. The matching engine logic lives in engine/.

Market owns a single market's state.
OrderBook stores and matches active orders.
Order represents a limit order.
Trade represents a completed match.
Position tracks user YES/NO exposure.

## Matching behavior

Orders are matched when the best BUY price is greater than or equal to the best SELL price.

BUY orders are prioritized by highest price, then earliest order_id.
SELL orders are prioritized by lowest price, then earliest order_id.

Trades execute at the resting order's price.

## Edge cases handled

- Partial fills
- Full fills
- Cancelling resting orders
- Short YES positions are allowed, so users can sell YES even without owning YES first

## If I had more time

- Add stronger HTTP error handling with HTTPException
- Add persistence instead of in-memory dictionaries
- Add explicit NO contract support
- Add self-trade prevention
- Add concurrency/race-condition handling
- Add automated tests