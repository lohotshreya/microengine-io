import random
import uuid
from engine.order import Order

class MarketSimulator:
    def __init__(self, base_price: float = 150.0):
        self.current_price = base_price
        self.order_counter = 0

    def generate_order_stream(self, systemic_shock: bool = False) -> Order:
        self.order_counter += 1
        order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        
        # Standard noise simulation vs institutional sweeping shock
        if systemic_shock:
            # Massive sell-side liquidation event draining buy interest
            side = 'SELL'
            price = self.current_price * random.uniform(0.92, 0.96)
            quantity = random.randint(5000, 12000)
        else:
            side = random.choices(['BUY', 'SELL'], weights=[0.5, 0.5])[0]
            price_offset = random.uniform(0.01, 2.50)
            price = self.current_price + price_offset if side == 'SELL' else self.current_price - price_offset
            quantity = random.randint(10, 500)
            
            # Natural micro-drift
            self.current_price += random.uniform(-0.15, 0.15)
            
        return Order(order_id, side, price, quantity)
