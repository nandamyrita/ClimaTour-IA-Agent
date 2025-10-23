import os
from dotenv import load_dotenv
import pytest
from tools.weather_tool import get_weather_by_state

load_dotenv()  

def test_weather_sp():
    estado = "rio de janeiro"
    resultado = get_weather_by_state(estado)
    
    
    assert "error" not in resultado, "Chave da API OpenWeather não definida ou inválida."
    
    assert "cidade" in resultado
    assert "temperatura" in resultado
    assert "descrição" in resultado
    assert "umidade" in resultado
    assert "vento" in resultado
    
    print(resultado)
