# 🌍 ClimaTour - Assistente de Viagem Inteligente

Chatbot assistente de viagem que recomenda passeios turísticos baseados no estado do usuário e condições climáticas atuais.

## 🚀 Tecnologias

- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui**
- **Lucide Icons**

## 📦 Instalação

```bash
npm install
# ou
yarn install
# ou
pnpm install
```

## 🏃‍♂️ Executar o projeto

```bash
npm run dev
# ou
yarn dev
# ou
pnpm dev
```

Abra [http://localhost:3000](http://localhost:3000) no navegador.

## ⚙️ Configuração do Backend Python

A aplicação está configurada para se conectar ao backend Python em:
```
http://localhost:8000/chat
```

Para configurar a URL da API, edite o arquivo:
```
/components/ChatInterface.tsx (linha 24)
```

Consulte o arquivo `API_CONFIG.md` para mais detalhes sobre como conectar seu backend Python.

## 📁 Estrutura do Projeto

```
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Layout raiz
│   └── page.tsx           # Página principal
├── components/            # Componentes React
│   ├── ChatInterface.tsx  # Interface do chat
│   ├── ChatMessage.tsx    # Mensagem individual
│   ├── WelcomeScreen.tsx  # Tela de boas-vindas
│   └── ui/               # Componentes shadcn/ui
├── styles/
│   └── globals.css       # Estilos globais
└── API_CONFIG.md         # Documentação da API
```

## 🎨 Funcionalidades

- ✅ Interface de chat moderna e responsiva
- ✅ Design profissional similar ao ChatGPT/WhatsApp
- ✅ Suporte mobile, tablet e desktop
- ✅ Integração com API Python via REST
- ✅ Mensagens em tempo real
- ✅ Indicador de digitação
- ✅ Scroll automático
- ✅ Tratamento de erros

## 🔧 Desenvolvimento

Este é um projeto Next.js. Para modificar:
- Edite `app/page.tsx` para alterar a página principal
- Edite componentes em `/components`
- Estilos globais em `/styles/globals.css`

## 📝 Licença

MIT
