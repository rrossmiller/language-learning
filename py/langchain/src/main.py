import os
import tomllib

from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

with open("../openai.toml", "rb") as f:
    cfg = tomllib.load(f)

openai_key = cfg["openai_key"]

if __name__ == "__main__":
    os.system("clear")

    prompt = PromptTemplate(
        template="""You are a surfer dude, having a conversation about the surf conditions on the beach.
    Respond using surfer slang.

    Chat History: {chat_history}
    Context: {context}
    Question: {question}
    """,
        input_variables=["chat_history", "context", "question"],
    )
    chat_llm = ChatOpenAI(api_key=openai_key)

    memory = ConversationBufferMemory(
        memory_key="chat_history", input_key="question", return_messages=True
    )

    chat_chain = LLMChain(llm=chat_llm, prompt=prompt, memory=memory)
