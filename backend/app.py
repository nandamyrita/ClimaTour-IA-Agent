import os
import threading
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from backend.prompts import SISTEM_PROMPT
from backend.tools.weather_tool import get_weather_by_state

load_dotenv()

REQ_LIMIT = 10 
req_count = 0
req_lock = threading.Lock()
chat_histories = {} 

# Reseta o contador de requisições a cada minuto
def reset_req_count():
    global req_count
    with req_lock:
        req_count = 0
    threading.Timer(60, reset_req_count).start()

# Limite de requisições
def chamar_agent_com_limite(agent, agent_input): 
    global req_count
    with req_lock:
        if req_count >= REQ_LIMIT:
            return "Desculpe, o limite de requisições por minuto foi atingido. Tente novamente mais tarde."
        req_count += 1
    try:
        response = agent.invoke(agent_input) 
        return response
    except Exception as e:
        with req_lock:
            req_count -= 1
        return f"Erro inesperado: {e}"

# Conecta com o frontend
app = FastAPI() 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "")
        user_id = data.get("user_id", "default")

        if isinstance(user_input, list):
            user_input = " ".join(str(x) for x in user_input)
        else:
            user_input = str(user_input)

        user_input = user_input.strip()

        # Condições de saida para o chat
        if user_input.lower() == "sair":
            chat_histories.pop(user_id, None)
            return {"response": "👋 Até mais! Chat finalizado com sucesso."}

        from backend.tools.weather_tool import _normalize_state_name, STATE_TO_CITY
        state_norm = _normalize_state_name(user_input)

        if state_norm not in STATE_TO_CITY:
            return {"response": f"Opa! 😅 Não encontrei o estado '{user_input}'. Verifique se está escrito corretamente ou digite 'sair' para encerrar o chat!"}



        current_history = chat_histories.get(user_id, [])
        
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            return {"response": "Erro: Chave da API Google (GOOGLE_API_KEY) não encontrada."}
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=google_api_key
        )
        tools = [get_weather_by_state]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", SISTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"), 
            ("user", "{input}"),                       
            MessagesPlaceholder(variable_name="agent_scratchpad") 
        ])
        
        agent_runnable = create_tool_calling_agent(llm, tools, prompt)
        
        agent = AgentExecutor(
            agent=agent_runnable, 
            tools=tools, 
            verbose=False
        )
        
        agent_input = {
            "messages": current_history,
            "input": user_input        
        }
        
        response = chamar_agent_com_limite(agent, agent_input)

        ai_message = ""
        if isinstance(response, str): 
            ai_message = response
        elif isinstance(response, dict):
            ai_message = response.get("output", "Desculpe, não consegui processar sua resposta.")
        else:
            ai_message = str(response)

        if user_id not in chat_histories:
            chat_histories[user_id] = []
        chat_histories[user_id].append({"role": "user", "content": user_input})
        chat_histories[user_id].append({"role": "assistant", "content": ai_message})

        return {"response": ai_message}

    except Exception as e:
        return {"response": f"Erro interno: {e}"}