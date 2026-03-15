# hello.py
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# 1. Istanzia il modello
llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=512)

# 2. Costruisci i messaggi
messages = [
    SystemMessage(content="Sei un assistente cordiale. Rispondi in italiano."),
    HumanMessage(content="Ciao! Cosa sai fare?")
]

# 3. Invoca
response = llm.invoke(messages)

print(response.content)       # il testo della risposta
print(type(response))         # → AIMessage
