from engine.order import Order
from engine.order_book import OrderBook

class MatchingEngine:
    def __init__(self):
        self.book = OrderBook()
        self.trade_history = []

    def process_order(self, incoming_order: Order):
        if incoming_order.side == 'BUY':
            self._match_order(incoming_order, self.book._asks, is_buy=True)
        else:
            self._match_order(incoming_order, self.book._bids, is_buy=False)

    def _match_order(self, incoming: Order, opposite_queue, is_buy: bool):
        trades_to_execute = []
        prices_to_clear = []

        for price, orders_at_price in opposite_queue.items():
            actual_price = -price if not is_buy else price
            
            # Check execution condition (Bid >= Ask)
            if is_buy and incoming.price < actual_price:
                break
            if not is_buy and incoming.price > actual_price:
                break

            for resting_order in list(orders_at_price):
                match_qty = min(incoming.quantity, resting_order.quantity)
                incoming.quantity -= match_qty
                resting_order.quantity -= match_qty

                trades_to_execute.append({
                    "price": actual_price,
                    "quantity": match_qty,
                    "buyer_id": incoming.order_id if is_buy else resting_order.order_id,
                    "seller_id": resting_order.order_id if is_buy else incoming.order_id
                })

                if resting_order.quantity == 0:
                    orders_at_price.remove(resting_order)
                    self.book.order_map.pop(resting_order.order_id, None)

                if incoming.quantity == 0:
                    break

            if not orders_at_price:
                prices_to_clear.append(price)
            if incoming.quantity == 0:
                break

        # Clean empty price levels from internal queues
        for price in prices_to_clear:
            del opposite_queue[price]

        self.trade_history.extend(trades_to_execute)

        # If order is not completely filled, add remaining depth to order book
        if incoming.quantity > 0:
            self.book.add_order(incoming)
