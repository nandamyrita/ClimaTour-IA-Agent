# 🌤️ ClimaTour — Guia de Viagens Inteligente com IA

O **ClimaTour** é um assistente de viagens que usa **IA e dados climáticos em tempo real** para sugerir atividades personalizadas com base no clima de cada estado do Brasil.
Desenvolvido com **FastAPI**, **LangChain** e **Gemini AI**, ele oferece uma experiência interativa e dinâmica.

---

## 🚀 Funcionalidades

* Consulta de clima em tempo real por estado brasileiro 🌦️
* Recomendações personalizadas de passeios com base no clima 🏖️
* Detecção e tratamento de erros amigáveis 😅
* Histórico de conversa por usuário 💬
* Interface responsiva com Vite + React ⚡
* Integração direta com **Gemini AI (Google)** 🤖

---

## 🧩 Estrutura do Projeto

```
climatour/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── prompts.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── weather_tool.py
│   └── tests/
│       └── test_weather.py
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       └── components/
│           └── ...
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

* [Python 3.11](https://www.python.org/downloads/)
* [Node.js 18+](https://nodejs.org/)
* [npm](https://www.npmjs.com/)
* Uma chave de API do **Gemini AI** (Google AI Studio)

---

## 🔑 Configuração do Ambiente

Crie um arquivo `.env` na pasta **backend/** com o seguinte conteúdo:

```bash
GOOGLE_API_KEY=YOUR_API_KEY_HERE
OPENWEATHER_API_KEY=YOUR_OPENWEATHER_KEY_HERE
```

> 💡 Substitua pelos valores reais das suas chaves de API.

---

## 🐍 Instalação do Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

---

## 💻 Rodando o Servidor Backend

```bash
uvicorn backend.app:app --reload
```

O servidor será iniciado em:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🌐 Instalação do Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

A aplicação estará disponível em:
👉 **[http://localhost:5173](http://localhost:5173)**

---

## 🧪 Executando Testes

```bash
pytest backend/tests/test_weather.py
```

---

## 🧠 Exemplo de Interação

**Usuário:**

> Quero saber o clima em São Paulo.

**ClimaTour:**

> Que notícia maravilhosa! ☀️ O clima em São Paulo está ensolarado com 26°C.
> É o dia perfeito para curtir ao ar livre! Que tal explorar o Parque Ibirapuera ou fazer um passeio de bicicleta pela orla?

---

## 🧰 Tecnologias Utilizadas

| Área     | Tecnologias                           |
| -------- | ------------------------------------- |
| Backend  | FastAPI, LangChain, Gemini AI, Python |
| Frontend | React, Vite, Tailwind CSS             |
| APIs     | OpenWeatherMap, Google Generative AI  |
| Testes   | Pytest                                |

---

## ✨ Créditos

Desenvolvido com 💙 por **Maria Fernanda**
🤖 *Powered by IA • 🌤️ Dados em tempo real*
