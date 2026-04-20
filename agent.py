"""
agent.py  —  MediBot LLM Agent

Changes vs original:
  - Uses a system prompt to keep answers grounded in the retrieved context
  - Slightly lower temperature (0.1) for more factual, focused answers
  - max_iterations bumped to 7 so the agent has room to use both tools
"""

import os
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

from rag_tool import rag_tool
from tools import symptom_tool

# ── API key check ─────────────────────────────────────────────────────────────
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise EnvironmentError(
        "GROQ_API_KEY not set.\n"
        "Get a free key at https://console.groq.com then run:\n"
        "  Windows : set GROQ_API_KEY=your_key_here\n"
        "  Mac/Linux: export GROQ_API_KEY=your_key_here"
    )

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,          # lower = more factual, less hallucination
    api_key=SecretStr(api_key),
    stop_sequences=[],
)

# ── Memory ────────────────────────────────────────────────────────────────────
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

# ── System / prefix prompt ────────────────────────────────────────────────────
SYSTEM_PREFIX = (
    "You are MediBot, a helpful medical information assistant. "
    "Always base your answers on the information returned by your tools. "
    "If a tool returns relevant passages, summarise and cite them. "
    "Never fabricate medical facts. "
    "Always remind the user to consult a qualified healthcare professional "
    "for personal medical advice or diagnosis."
)

# ── Agent ─────────────────────────────────────────────────────────────────────
agent = initialize_agent(
    tools=[rag_tool, symptom_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=7,           
    agent_kwargs={
        "prefix": SYSTEM_PREFIX
    }
)


def run_agent(query: str) -> str:
    result = agent.invoke({"input": query})
    return result.get("output", str(result))