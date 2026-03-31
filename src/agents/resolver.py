from langchain_core.messages import HumanMessage, SystemMessage

from services.knowledge_base import KnowledgeBase
from services.llm_client import LLMClient
from state import State

def resolve(state: State, llm_client: LLMClient, knowledge_base_client: KnowledgeBase) -> State:
    relevant_contexts = knowledge_base_client.search(state["user_message"])
    splited_contexts = "\n".join(relevant_contexts)

    system_message = SystemMessage(content=f"""
        Você é Max, assistente da VanParts...

        Use o contexto abaixo para responder:
        {splited_contexts}

        Se não souber, diga que vai verificar.
    """)

    user_message = HumanMessage(state["user_message"])

    messages = [
        system_message,
        user_message
    ]

    state["resolution"] = llm_client.call(messages).content

    return state