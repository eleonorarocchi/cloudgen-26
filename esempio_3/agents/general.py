# agents/general.py

# Agente stateless: riceve il messaggio, risponde, stop.

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, AIMessage
from state import State

# Risponde a saluti e domande generiche
def general_node(state: State, llm: ChatAnthropic) -> dict:
    """Risponde a saluti e domande generiche."""
    r = llm.invoke([
        SystemMessage(content="Sei un assistente cordiale. Rispondi in italiano."),
        *state["messages"]
    ])
    return {"messages": [AIMessage(content=r.content)]}