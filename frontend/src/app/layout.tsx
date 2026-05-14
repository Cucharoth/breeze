import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Breeze-RP | Minimalist Branching Narratives",
  description: "A privacy-first, minimalist roleplay interface with branching timelines and hybrid memory.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="gradient-blob" />
        {children}
      </body>
    </html>
  );
}
