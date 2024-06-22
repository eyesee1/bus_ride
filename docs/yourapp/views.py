from messagebus import MessageBus
from .commands import AddItemToCart


def add_item_to_cart_view(request):
    command = AddItemToCart(
        cart_id=request.session["cart_id"],
        item_id=request.POST.get("item_id"),
        qty=request.POST.get("quantity", 1),
    )
    bus = MessageBus(command)
    result = bus()
    cart_item_id = result[0].data
    return {"result": "OK", "cart_item_id": cart_item_id}
