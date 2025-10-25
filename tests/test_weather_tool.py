import pytest
from unittest.mock import patch
from backend.tools.weather_tool import get_weather_by_state, _normalize_state_name, _map_weather_condition

def test_normalize_state_name():
    assert _normalize_state_name("São Paulo") == "sao paulo"
    assert _normalize_state_name("   Ceará  ") == "ceara"
    assert _normalize_state_name("MATO GROSSO") == "mato grosso"

def test_map_weather_condition():
    assert _map_weather_condition("céu limpo") == "Céu Limpo"
    assert _map_weather_condition("few clouds") == "Parcialmente Nublado"
    assert _map_weather_condition("chuva leve") == "Chuvoso"
    assert _map_weather_condition("mist") == "Nebuloso"
    assert _map_weather_condition("neve") == "Nevando"
    assert _map_weather_condition("condição desconhecida") == "Condição desconhecida"

@patch("backend.tools.weather_tool.requests.get")
def test_get_weather_by_state_success(mock_get, monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake_key")
    mock_response = {"main": {"temp": 25.5}, "weather": [{"description": "céu limpo"}]}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    result = get_weather_by_state("São Paulo")
    assert "Céu Limpo" in result
    assert "25.5°C" in result

@patch("backend.tools.weather_tool.requests.get")
def test_get_weather_invalid_state(mock_get, monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake_key")
    result = get_weather_by_state("Atlantis")
    assert "não reconhecido" in result.lower()

def test_get_weather_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    result = get_weather_by_state("São Paulo")
    assert "não encontrada" in result.lower()

@patch("backend.tools.weather_tool.requests.get")
def test_get_weather_api_error(mock_get, monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake_key")
    mock_get.side_effect = Exception("Erro simulado")
    result = get_weather_by_state("Bahia")
    assert "erro inesperado" in result.lower()
