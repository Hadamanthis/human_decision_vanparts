from pydantic import BaseModel

from langchain_core.messages import HumanMessage, SystemMessage

from services.knowledge_base import KnowledgeBase
from services.llm_client import LLMClient
from state import State

class Product(BaseModel):
    name: str | None
    price: float | None

def resolve(state: State, llm_client: LLMClient, knowledge_base_client: KnowledgeBase) -> State:
    user_message = HumanMessage(state["user_message"])

    if state["intention"] == "reembolso":

        # Busca contexto para a LLM
        product_context = knowledge_base_client.search(state["user_message"], n_results=1, source="produtos")[0]

        system_message = SystemMessage(content=f"""
            Você é Max, assistente da VanParts.
    
            O cliente quer um reembolso. Com base no contexto abaixo, identifique:
            - O nome exato do produto mencionado
            - O preço do produto conforme consta no contexto
            
            Contexto:
            {product_context}
            
            Se não encontrar o produto ou preço no contexto, retorne null.
        """)

        messages = [
            system_message,
            user_message
        ]

        product_json = llm_client.call_structured(messages, Product)

        state["product"] = product_json.name
        state["price"] = product_json.price
        state["resolution"] = "Tentativa de Reembolso"

    elif state["intention"] == "duvida" or state["intention"] == "elogio":
        # Busca contexto para a LLM
        contexts = knowledge_base_client.search(state["user_message"], n_results=3)
        splited_contexts = "\n".join(contexts)

        system_message = SystemMessage(content=f"""
            Você é Max, assistente da VanParts...

            Use o contexto abaixo para responder:
            {splited_contexts}

            Se não souber, diga que vai verificar.
        """)

        messages = [
            system_message,
            user_message
        ]

        result = llm_client.call(messages).content

        state["resolution"] = result
    else:
        system_message = SystemMessage(content=f"""
            Você é Max, assistente da VanParts...
                                       
            O usuário não deu contexto suficiente sobre se gostaria de fazer um elogio, tirar uma dúvida ou se queria um reembolso.
                                       
            Deixe claro que não pode responder a ele devido a esse fato e agradeça o contato
        """)

        messages = [
            system_message,
            user_message
        ]

        response = llm_client.call(messages).content

        state["resolution"] = response
        

    return state