from typing import Type, TypeVar

from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
import dotenv

T = TypeVar("T") # Tipo genérico antes do python 3.12

class LLMClient:
    def __init__(self):
        self.model = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0
        )

    def call(self, messages: list[BaseMessage]) -> str:
        return self.model.invoke(messages)
    
    def call_structured(self, messages: list[BaseMessage], schema: Type[T]) -> T:
        structured_llm = self.model.with_structured_output(schema)
        return structured_llm.invoke(messages)