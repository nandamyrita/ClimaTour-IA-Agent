import os
import requests
from requests.exceptions import RequestException, HTTPError, JSONDecodeError
from typing import Dict, Any, Union, TypedDict
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


STATE_TO_CITY = {
    "acre": "Rio Branco",
    "alagoas": "Maceió",
    "amapa": "Macapá",
    "amazonas": "Manaus",
    "bahia": "Salvador",
    "ceara": "Fortaleza",
    "distrito federal": "Brasília",
    "espirito santo": "Vitória",
    "goias": "Goiânia",
    "maranhao": "São Luís",
    "mato grosso": "Cuiabá",
    "mato grosso do sul": "Campo Grande",
    "minas gerais": "Belo Horizonte",
    "para": "Belém",
    "paraiba": "João Pessoa",
    "parana": "Curitiba",
    "pernambuco": "Recife",
    "piaui": "Teresina",
    "rio de janeiro": "Rio de Janeiro",
    "rio grande do norte": "Natal",
    "rio grande do sul": "Porto Alegre",
    "rondonia": "Porto Velho",
    "roraima": "Boa Vista",
    "santa catarina": "Florianópolis",
    "sao paulo": "São Paulo",
    "sergipe": "Aracaju",
    "tocantins": "Palmas"
}



class WeatherData(TypedDict):
    cidade: str
    temperatura: float
    descricao: str
    umidade: int
    vento: float


class ErrorData(TypedDict):
    error: str


WeatherResponse = Union[WeatherData, ErrorData]



def _normalize_state_name(state_name: str) -> str:
    
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ç': 'c',
        'â': 'a', 'ê': 'e', 'ô': 'o', 'ã': 'a', 'õ': 'o'
    }
    state_norm = state_name.lower().strip()
    for accented, unaccented in replacements.items():
        state_norm = state_norm.replace(accented, unaccented)
    return state_norm

def _map_weather_condition(description: str) -> str:
    
    desc_lower = description.lower()
    
    if any(k in desc_lower for k in ["céu limpo", "ensolarado"]):
        return "Ensolarado"
    
    elif any(k in desc_lower for k in ["chuva", "garoa", "tempestade", "trovoada"]):
        return "Chuvoso"
    elif any(k in desc_lower for k in ["nublado", "nuvens"]):
        return "Nublado"
    elif any(k in desc_lower for k in ["névoa", "nevoeiro"]):
        return "Nevoeiro"
    else:
        
        return description.capitalize()



def get_weather_by_state(state_name: str) -> WeatherResponse:
    
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "Chave da API OpenWeather (OPENWEATHER_API_KEY) não encontrada no ambiente."}
    
    
    state_norm = _normalize_state_name(state_name)
    city = STATE_TO_CITY.get(state_norm)
    
    if not city:
        return {"error": f"Estado '{state_name}' não reconhecido ou não mapeado."}

    
    params = {
        "q": f"{city},BR",
        "appid": api_key,
        "units": "metric", 
        "lang": "pt_br"      
    }

    try:
        resp = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        
        resp.raise_for_status() 
        data = resp.json()

    
    except HTTPError as e:
        if e.response.status_code == 401:
            return {"error": "Chave da API inválida ou não autorizada."}
        elif e.response.status_code == 404:
            return {"error": f"Cidade '{city}' não encontrada na API de clima."}
        else:
            return {"error": f"Erro HTTP ao buscar dados: {e.response.status_code}"}
    except RequestException:
        
        return {"error": "Erro de conexão com a API de clima."}
    except JSONDecodeError:
        return {"error": "Resposta inválida (não-JSON) recebida da API de clima."}
    
    
    try:
        temperatura = data["main"]["temp"]
        umidade = data["main"]["humidity"]
        vento = data["wind"]["speed"]
        
        condicao_raw = data["weather"][0]["description"]

        condicao_mapeada = _map_weather_condition(condicao_raw)

        
        return {
            "cidade": city,
            "temperatura": round(temperatura, 1),
            "descricao": condicao_mapeada,
            "umidade": umidade,
            "vento": round(vento * 3.6, 1) 
        }
    
    except KeyError:
        
        return {"error": "Estrutura de dados inesperada recebida da API."}
    except Exception as e:
        
        return {"error": f"Erro interno ao processar dados: {e}"}


if __name__ == "__main__":

    weather_sp = get_weather_by_state("São Paulo")
    print(f"Clima em São Paulo: {weather_sp}")

    
    weather_sc = get_weather_by_state("SANTA CATARINA")
    print(f"Clima em Santa Catarina: {weather_sc}")

    
    weather_err = get_weather_by_state("Terra do Nunca")
    print(f"Clima em Terra do Nunca: {weather_err}")
