from attrs import define, field

from messagebus import Command, Receiver, ReceiverReturnType, ReturnMessage


@define
class AddItemToCart(Command):
    cart_id: int = field()
    item_id: int = field()
    qty: int = field()


@define
class AddItemToCartReceiver(Receiver):
    command: AddItemToCart = field()

    handles_command_cls = AddItemToCart

    def execute_command(self) -> ReceiverReturnType:
        from ..events.item_added_to_cart import ItemAddedToCart

        cart_item_id = self._save_item_to_cart()
        return [
            ReturnMessage(data=cart_item_id),
            ItemAddedToCart(cart_item_id=cart_item_id),
        ]

    def _save_item_to_cart(self) -> int:
        # pretend we actually saved it
        return 1
