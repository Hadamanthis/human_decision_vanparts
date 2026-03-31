from state import State


def final_response(state: State) -> State:
    match state["approved"]:
        case True:
            state["final_message"] = "Reembolso confirmado. Aguarde email com mais informações."
        case False:
            state["final_message"] = "Reembolso negado. Aguarde email com mais informações."
        case None:
            state["final_message"] = state["resolution"]
    
    return state