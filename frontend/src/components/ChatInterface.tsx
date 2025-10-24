"use client";

import { useState, useRef, useEffect } from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Send, CloudSun, Sparkles } from "lucide-react";
import { ChatMessage } from "./ChatMessage";
import { WelcomeScreen } from "./WelcomeScreen";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // URL do backend 
  const BACKEND_URL = "http://localhost:8000/chat";

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.content,
          
        }),
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }

      const data = await response.json();

      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response || data.message, // Ajuste conforme retorno da sua API
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      
      if (process.env.NODE_ENV === 'development') {
        console.warn("⚠️ Backend não conectado:", BACKEND_URL);
      }
      
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `❌ **Erro de conexão**\n\nNão foi possível conectar ao backend em:\n\`${BACKEND_URL}\`\n\n**Soluções:**\n✅ Verifique se seu servidor Python está rodando\n✅ Confirme a URL da API no código\n✅ Verifique as configurações de CORS`,
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleStartConversation = () => {
    const welcomeMessage: Message = {
      id: Date.now().toString(),
      role: "assistant",
      content: "Olá! Sou o ClimaTour, seu assistente de viagem inteligente. 🌍✨\nPara começar, me diga: de qual estado brasileiro você é?",
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
   
      <div className="bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 shadow-lg flex-shrink-0">
        <div className="container mx-auto max-w-5xl px-3 sm:px-4 md:px-6 py-3 sm:py-4">
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-white rounded-full flex items-center justify-center shadow-md flex-shrink-0">
              <CloudSun className="w-5 h-5 sm:w-7 sm:h-7 text-blue-600" />
            </div>
            <div className="flex-1 min-w-0">
              <h1 className="text-white truncate">ClimaTour</h1>
              <div className="flex items-center gap-1.5 sm:gap-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse flex-shrink-0" />
                <p className="text-blue-100 text-xs sm:text-sm truncate">Assistente Online</p>
              </div>
            </div>
            <Sparkles className="w-5 h-5 sm:w-6 sm:h-6 text-yellow-300 flex-shrink-0" />
          </div>
        </div>
      </div>

      
      <div className="flex-1 overflow-hidden flex flex-col">
        {messages.length === 0 ? (
          <WelcomeScreen onStart={handleStartConversation} />
        ) : (
          <>
            
            <div className="flex-1 overflow-y-auto">
              <div className="container mx-auto max-w-5xl px-3 sm:px-4 md:px-6 py-4 sm:py-6">
                <div className="space-y-4 sm:space-y-6">
                  {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                  ))}
                  {isLoading && (
                    <div className="flex items-start gap-2 sm:gap-3">
                      <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center flex-shrink-0 shadow-md">
                        <CloudSun className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
                      </div>
                      <div className="bg-white rounded-2xl rounded-tl-sm px-3 sm:px-4 py-2 sm:py-3 shadow-sm max-w-[80%]">
                        <div className="flex items-center gap-2">
                          <div className="flex gap-1">
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                          </div>
                          <span className="text-xs sm:text-sm text-gray-500">Pensando...</span>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              </div>
            </div>

            
            <div className="border-t bg-white flex-shrink-0 shadow-lg">
              <div className="container mx-auto max-w-5xl px-3 sm:px-4 md:px-6 py-3 sm:py-4">
                <div className="flex gap-2 sm:gap-3 items-end">
                  <div className="flex-1 min-w-0">
                    <Input
                      ref={inputRef}
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Digite sua mensagem..."
                      disabled={isLoading}
                      className="rounded-full h-11 sm:h-12 px-4 sm:px-5 border-gray-300 focus:border-blue-500 shadow-sm w-full"
                    />
                  </div>
                  <Button
                    onClick={sendMessage}
                    disabled={!input.trim() || isLoading}
                    className="rounded-full w-11 h-11 sm:w-12 sm:h-12 p-0 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 shadow-md flex-shrink-0"
                  >
                    <Send className="w-4 h-4 sm:w-5 sm:h-5" />
                  </Button>
                </div>
                <p className="text-xs text-gray-400 mt-2 text-center truncate">
                  Backend: {BACKEND_URL}
                </p>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
