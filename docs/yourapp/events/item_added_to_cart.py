from attrs import define, field

from messagebus import Event, Handler, HandlerReturnType


@define
class ItemAddedToCart(Event):
    cart_item_id: int = field()


class ItemAddedToCartHandler(Handler):
    event: ItemAddedToCart = field()

    handles_events = [ItemAddedToCart]

    def handle_event(self) -> HandlerReturnType:
        self._notify_sales_team()
        return []

    def _notify_sales_team(self) -> None:
        # obviously you would do something real here:
        print(f"We got one! {self.event}")
