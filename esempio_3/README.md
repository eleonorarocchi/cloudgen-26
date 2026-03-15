# ESEMPIO 2

## 1. Crea un ambiente virtuale (SEMPRE farlo, è buona pratica)
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# oppure: venv\Scripts\activate  # Windows

## 2. Installa le dipendenze
pip3 install langchain langchain-anthropic fastapi uvicorn python-dotenv langgraph

## 3. Esegui
uvicorn main:app --reload

## 4. domande
Quanto costa il piano Pro?
Vorrei essere ricontattata
Mi interessa il piano Enterprise
eleonora@esempio.it
