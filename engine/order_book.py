from sortedcontainers import SortedDict
from engine.order import Order

class OrderBook:
    def __init__(self):
        # Bids: Highest price first -> negative price keys for descending order
        self._bids = SortedDict(lambda price: -price)
        # Asks: Lowest price first -> standard ascending order
        self._asks = SortedDict()
        
        # Fast lookup map to locate orders by ID: {order_id: Order}
        self.order_map = {}

    def add_order(self, order: Order):
        self.order_map[order.order_id] = order
        target_queue = self._bids if order.side == 'BUY' else self._asks
        
        if order.price not in target_queue:
            target_queue[order.price] = []
        target_queue[order.price].append(order)

    def cancel_order(self, order_id: str) -> bool:
        if order_id not in self.order_map:
            return False
        
        order = self.order_map.pop(order_id)
        target_queue = self._bids if order.side == 'BUY' else self._asks
        
        if order.price in target_queue:
            orders_at_price = target_queue[order.price]
            orders_at_price.remove(order)
            if not orders_at_price:
                del target_queue[order.price]
            return True
        return False

    def get_depth(self, levels: int = 5):
        """Returns top N levels of bids and asks for market depth visualization."""
        bid_depth = []
        for price, orders in self._bids.items():
            # Adjust back from the internal negative sorting key
            actual_price = -price
            total_vol = sum(o.quantity for o in orders)
            bid_depth.append({'Price': actual_price, 'Volume': total_vol})
            if len(bid_depth) >= levels:
                break
                
        ask_depth = []
        for price, orders in self._asks.items():
            total_vol = sum(o.quantity for o in orders)
            ask_depth.append({'Price': price, 'Volume': total_vol})
            if len(ask_depth) >= levels:
                break
                
        return bid_depth, ask_depth

    @property
    def best_bid(self):
        return -self._bids.iloc[0] if self._bids else None

    @property
    def best_ask(self):
        return self._asks.iloc[0] if self._asks else None
