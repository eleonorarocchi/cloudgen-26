# agents/router.py
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from state import State


def router_node(state: State, llm: ChatAnthropic) -> dict:
    # Se il flusso contatto è già aperto, non ri-classificare
    if state.get("contact_step") in ("ask_reason", "ask_email"):
        return {"intent": "contact"}

    intent = llm.invoke([
        SystemMessage(content=(
            "Classifica il messaggio in UNA parola sola.\n\n"
            "'kb_search' → l'utente chiede informazioni su prezzi, piani, "
            "funzionalità, trial gratuito, supporto, assistenza.\n\n"
            "'contact' → l'utente vuole essere ricontattato, parlare con "
            "qualcuno, sentire un commerciale, fare una richiesta, essere "
            "chiamato, mandare una email. "
            "Esempi: 'vorrei essere ricontattata', 'posso parlare con un "
            "commerciale?', 'mandate qualcuno', 'voglio più informazioni "
            "da una persona'.\n\n"
            "'general' → tutto il resto: saluti, domande generiche, "
            "conversazione.\n\n"
            "Rispondi SOLO con una di queste tre parole: "
            "kb_search, contact, general"
        )),
        HumanMessage(content=state["messages"][-1].content)
    ]).content.strip().lower()

    if intent not in ("kb_search", "contact", "general"):
        intent = "general"

    return {"intent": intent}
