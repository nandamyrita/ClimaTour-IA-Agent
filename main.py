import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_core.utils.input import GStr
from tools.weather_tool import get_weather_by_state
from prompts import agent_prompt

def main():
    load_dotenv()

    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Por favor, defina a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS com o caminho para suas credenciais do Google.")
        return
    if not os.getenv("OPENWEATHER_API_KEY"):
        print("Por favor, defina a variável de ambiente OPENWEATHER_API_KEY com sua chave da API OpenWeather.")
        return
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    tools = [
        Tool(
            name= "get_weather_by_state",
            func=get_weather_by_state,
            description="Use esta ferramenta para obter o clima atual na capital de um estado brasileiro. O input é o nome do estado em português.",
        )
    ]

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    agent = create_react_agent(llm, tools, agent_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )

    print("Bem-vindo ao ClimaTour! Seu assistente de viagens especializado em clima e turismo no Brasil. 🌞🌧️")
    print("Pergunte-me sobre o clima em qualquer estado brasileiro e receba recomendações de passeios!")
    print("Digite 'sair' para encerrar.")

    while True:
        try:
            user_input = input("\nVocê: ")
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("Obrigado por usar o ClimaTour! Até a próxima! 👋")
                break

            response = agent_executor.invoke({"input": GStr(user_input)})
            print(f"ClimaTour: {response['output']}")

        except Exception as e:
            print(f"Ops! Ocorreu um erro: {e}")
            print("Por favor, tente novamente.")

        if __name__ == "__main__":
                main()


            
