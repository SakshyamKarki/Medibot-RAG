import os
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

from rag_tool import rag_tool
from tools import symptom_tool

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise EnvironmentError(
        "GROQ_API_KEY not set.\n"
        "Get a free key at https://console.groq.com then run:\n"
        "  Windows : set GROQ_API_KEY=your_key_here\n"
        "  Mac/Linux: export GROQ_API_KEY=your_key_here"
    )

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=SecretStr(api_key),
    stop_sequences=[],
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

agent = initialize_agent(
    tools=[rag_tool, symptom_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)

def run_agent(query: str) -> str:
    result = agent.invoke({"input": query})
    return result.get("output", str(result))