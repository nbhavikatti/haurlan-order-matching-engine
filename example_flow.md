# Example Matching Flow

## Example 1: Resting sell order

Request:

```json
{
  "user_id": "seller1",
  "side": "SELL",
  "price": 0.80,
  "quantity": 10
}
```

Result: no trade occurs because there are no buy orders yet.

```json
{
  "buy_orders": [],
  "sell_orders": [
    {
      "order_id": 0,
      "user_id": "seller1",
      "side": "SELL",
      "price": 0.80,
      "quantity": 10
    }
  ]
}
```

## Example 2: Non-crossing buy order

Request:

```json
{
  "user_id": "buyer1",
  "side": "BUY",
  "price": 0.70,
  "quantity": 5
}
```

Result: no trade occurs because `0.70 < 0.80`.

```json
{
  "buy_orders": [
    {
      "order_id": 1,
      "user_id": "buyer1",
      "side": "BUY",
      "price": 0.70,
      "quantity": 5
    }
  ],
  "sell_orders": [
    {
      "order_id": 0,
      "user_id": "seller1",
      "side": "SELL",
      "price": 0.80,
      "quantity": 10
    }
  ]
}
```

## Example 3: Crossing buy order

Request:

```json
{
  "user_id": "buyer2",
  "side": "BUY",
  "price": 0.85,
  "quantity": 4
}
```

Result: a trade occurs because `0.85 >= 0.80`. The trade executes at the resting sell price, `0.80`.

Trade:

```json
{
  "trade_id": 0,
  "buyer_id": "buyer2",
  "seller_id": "seller1",
  "price": 0.80,
  "quantity": 4,
  "buy_order_id": 2,
  "sell_order_id": 0
}
```

Final order book:

```json
{
  "buy_orders": [
    {
      "order_id": 1,
      "user_id": "buyer1",
      "side": "BUY",
      "price": 0.70,
      "quantity": 5
    }
  ],
  "sell_orders": [
    {
      "order_id": 0,
      "user_id": "seller1",
      "side": "SELL",
      "price": 0.80,
      "quantity": 6
    }
  ]
}
```

Final positions:

```json
{
  "buyer2": {
    "yes_shares": 4,
    "no_shares": 0
  },
  "seller1": {
    "yes_shares": -4,
    "no_shares": 0
  }
}
```