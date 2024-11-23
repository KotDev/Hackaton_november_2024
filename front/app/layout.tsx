import type { Metadata } from "next";
import { Noto_Sans } from "next/font/google";
import "./globals.css";

const lato = Noto_Sans({
  subsets: ["latin"],
  variable: "--font-nunito",
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "Льгота.ру",
  description: "Помощь в поиске государственных льгот",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${lato.className} antialiased`}>
        <main className="min-h-screen">{children}</main>
      </body>
    </html>
  );
}
