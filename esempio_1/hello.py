# hello.py
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

print("Tracing:", os.getenv("LANGCHAIN_TRACING_V2"))
print("Key:", os.getenv("LANGCHAIN_API_KEY"))

# 1. Istanzia il modello
llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=512)

# 3. Leggi la domanda da terminale, es.: Ciao! Cosa sai fare?
domanda = input("Tu: ") 

# 2. Costruisci i messaggi
messages = [
    SystemMessage(content="Sei un assistente cordiale. Rispondi in italiano."),
    HumanMessage(content=domanda)
]

# 4. Invoca
response = llm.invoke(messages)

print(response.content)       # il testo della risposta
print(type(response))         # → AIMessage

# 5. Proviamo a vedere se ricorda, es.: Cosa ti ho chiesto?
domanda = input("Tu: ") 
messages = [
    HumanMessage(content=domanda)
]
response = llm.invoke(messages)
print(response.content)       # il testo della risposta
print(type(response))         # → AIMessage