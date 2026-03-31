from state import State
from services.llm_client import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage

system_message = SystemMessage(content="""
        Classifique a intenção do usuário em uma das categorias:

        - reembolso
        - duvida
        - elogio
        - desconhecido

        Responda APENAS com UMA das palavras acima.
        Se não tiver certeza, responda "desconhecido".

        NÃO escreva frases.
        NÃO explique.
        NÃO use pontuação.
        """)

def classify_intent(state: State, llm_client: LLMClient) -> State:
    user_message = HumanMessage(state["user_message"])

    messages = [
        system_message,
        user_message
    ]

    response = llm_client.call(messages)

    intention = response.content.strip().lower()

    match intention:
        case "reembolso" | "duvida" | "elogio" | "desconhecido":
            state["intention"] = intention
        case _:
            state["intention"] = "desconhecido"

    return state