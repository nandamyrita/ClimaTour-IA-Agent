import { CloudSun, User } from "lucide-react";
import { Message } from "./ChatInterface";
import { Avatar, AvatarFallback } from "./ui/avatar";

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-2 sm:gap-3 items-start ${isUser ? "flex-row-reverse" : ""}`}>
      <Avatar className={`w-8 h-8 sm:w-10 sm:h-10 flex-shrink-0 shadow-md ${
        isUser 
          ? "bg-gradient-to-br from-blue-600 to-blue-700" 
          : "bg-gradient-to-br from-cyan-500 to-blue-500"
      }`}>
        <AvatarFallback className="bg-transparent">
          {isUser ? (
            <User className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
          ) : (
            <CloudSun className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
          )}
        </AvatarFallback>
      </Avatar>

   
      <div className={`flex flex-col max-w-[75%] sm:max-w-[70%] md:max-w-[65%] ${isUser ? "items-end" : "items-start"}`}>
        {!isUser && (
          <span className="text-xs text-gray-600 mb-1 ml-1 px-1">ClimaTour</span>
        )}
        <div
          className={`rounded-2xl px-3 sm:px-4 md:px-5 py-2 sm:py-3 shadow-sm ${
            isUser
              ? "bg-gradient-to-br from-blue-600 to-blue-700 text-white rounded-tr-sm"
              : "bg-white text-gray-900 rounded-tl-sm border border-gray-100"
          }`}
        >
          <p className="whitespace-pre-wrap break-words leading-relaxed text-sm sm:text-base">
            {message.content}
          </p>
        </div>
        <span
          className={`text-xs mt-1 px-1 sm:px-2 ${
            isUser ? "text-gray-500" : "text-gray-400"
          }`}
        >
          {message.timestamp.toLocaleTimeString("pt-BR", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </div>
    </div>
  );
}
