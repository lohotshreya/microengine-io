import time

class Order:
    __slots__ = ['order_id', 'side', 'price', 'quantity', 'timestamp']
    
    def __init__(self, order_id: str, side: str, price: float, quantity: int):
        self.order_id = order_id
        self.side = side.upper()  # 'BUY' or 'SELL'
        self.price = round(price, 2)
        self.quantity = quantity
        self.timestamp = time.time_ns()

    def __repr__(self):
        return f"[{self.side}] ID: {self.order_id} | Price: {self.price} | Qty: {self.quantity}"
