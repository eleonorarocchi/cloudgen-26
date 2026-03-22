# ESEMPIO 2

## 1. Crea un ambiente virtuale (SEMPRE farlo, è buona pratica)
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# oppure: venv\Scripts\activate  # Windows
deactivate

## 2. Installa le dipendenze
python3 -m pip install langchain langchain-anthropic fastapi uvicorn python-dotenv langsmith

## 3. Esegui
python3 hello.py

## 4. Monitora
https://eu.smith.langchain.com