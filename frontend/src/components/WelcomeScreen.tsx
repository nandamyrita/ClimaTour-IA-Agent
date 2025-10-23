import { Button } from "./ui/button";
import { MapPin, CloudSun, Compass, Sparkles, MessageCircle } from "lucide-react";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";

interface WelcomeScreenProps {
  onStart: () => void;
}

export function WelcomeScreen({ onStart }: WelcomeScreenProps) {
  return (
    <div className="h-full flex items-center justify-center p-4 sm:p-6 md:p-8 bg-gradient-to-br from-blue-50 via-white to-cyan-50 overflow-y-auto">
      <div className="max-w-2xl w-full space-y-6 sm:space-y-8 text-center">
        {/* Robot Avatar */}
        <div className="flex justify-center">
          <div className="relative">
            <div className="w-20 h-20 sm:w-24 sm:h-24 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-full flex items-center justify-center shadow-2xl">
              <CloudSun className="w-11 h-11 sm:w-14 sm:h-14 text-white" />
            </div>
            <div className="absolute -bottom-1 -right-1 w-7 h-7 sm:w-8 sm:h-8 bg-green-500 rounded-full border-3 sm:border-4 border-white flex items-center justify-center">
              <Sparkles className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-white" />
            </div>
          </div>
        </div>

        {/* Title */}
        <div className="space-y-2 sm:space-y-3 px-4">
          <div className="flex items-center justify-center gap-2 flex-wrap">
            <h1 className="text-blue-600">ClimaTour</h1>
            <Badge className="bg-gradient-to-r from-blue-600 to-cyan-600 text-sm">IA</Badge>
          </div>
          <p className="text-gray-600 text-base sm:text-lg">
            Seu assistente de viagem inteligente
          </p>
          <p className="text-gray-500 text-sm sm:text-base px-2">
            Recomendações personalizadas de passeios baseadas no clima em tempo real
          </p>
        </div>

        {/* Features Cards */}
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4 mt-6 sm:mt-8 px-2">
          <Card className="p-4 sm:p-6 bg-white hover:shadow-lg transition-shadow">
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2 sm:mb-3">
              <MapPin className="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" />
            </div>
            <h3 className="text-gray-900 mb-1 sm:mb-2">Personalizado</h3>
            <p className="text-gray-600 text-xs sm:text-sm">
              Recomendações baseadas no seu estado
            </p>
          </Card>

          <Card className="p-4 sm:p-6 bg-white hover:shadow-lg transition-shadow">
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-cyan-100 rounded-full flex items-center justify-center mx-auto mb-2 sm:mb-3">
              <CloudSun className="w-5 h-5 sm:w-6 sm:h-6 text-cyan-600" />
            </div>
            <h3 className="text-gray-900 mb-1 sm:mb-2">Tempo Real</h3>
            <p className="text-gray-600 text-xs sm:text-sm">
              Dados climáticos atualizados
            </p>
          </Card>

          <Card className="p-4 sm:p-6 bg-white hover:shadow-lg transition-shadow sm:col-span-2 md:col-span-1">
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2 sm:mb-3">
              <Compass className="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" />
            </div>
            <h3 className="text-gray-900 mb-1 sm:mb-2">Inteligente</h3>
            <p className="text-gray-600 text-xs sm:text-sm">
              Sugestões ideais para você
            </p>
          </Card>
        </div>

        {/* CTA Button */}
        <div className="pt-2 sm:pt-4 px-4">
          <Button
            onClick={onStart}
            className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white px-8 sm:px-10 py-5 sm:py-6 shadow-xl hover:shadow-2xl transition-all w-full sm:w-auto"
          >
            <MessageCircle className="w-4 h-4 sm:w-5 sm:h-5 mr-2" />
            Iniciar Conversa
          </Button>
          <p className="text-xs text-gray-400 mt-3 sm:mt-4">
            🤖 Powered by IA • 🌤️ Dados em tempo real
          </p>
        </div>
      </div>
    </div>
  );
}
