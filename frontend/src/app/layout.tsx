import type { Metadata } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "ClimaTour - Assistente de Viagem Inteligente",
  description: "Recomendações personalizadas de passeios baseadas no clima em tempo real",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
