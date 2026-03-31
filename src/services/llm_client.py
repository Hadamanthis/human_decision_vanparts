from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
import dotenv

class LLMClient:
    def __init__(self):
        
        dotenv.load_dotenv()

        self.model = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0
        )

    def call(self, messages: list[BaseMessage]) -> str:
        response = self.model.invoke(messages)

        return response