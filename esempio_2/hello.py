# hello.py
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=512)

# La "memoria" è una semplice lista Python
history: list = [
    SystemMessage(content="Sei un assistente cordiale. Rispondi in italiano.")
]


def chat(user_input: str) -> str:
    # 1. Aggiungi il messaggio utente alla storia
    history.append(HumanMessage(content=user_input))

    # 2. Passa TUTTA la storia al modello
    response = llm.invoke(history)

    # 3. Aggiungi la risposta alla storia per ricordarla al prossimo giro
    history.append(AIMessage(content=response.content))

    return response.content


# Proviamo la memoria, es.: Ciao! Mi chiamo Eleonora.
domanda = input("Tu: ") 
print(chat(domanda))

print("---")

# Proviamo a vedere se ricorda, es.: Come mi chiamo?
domanda = input("Tu: ") 
print(chat(domanda))   # deve ricordare "Eleonora"

print("---")

# Proviamo a vedere se ricorda, es.: Qual era il mio saluto?
domanda = input("Tu: ") 

print(chat(domanda))  # deve ricordare "Ciao! Mi chiamo Eleonora."
