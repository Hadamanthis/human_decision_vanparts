from typing import TypedDict

class State(TypedDict):
    user_message: str
    intention: str | None
    resolution: str | None
    product: str | None
    price: float | None