from state import State

def evaluate_risk(state: State) -> State:
    product_price = state["price"]

    if product_price is None or product_price > 500:
        state["risk_level"] = "high"
    else:
        state["risk_level"] = "low"

    return state
