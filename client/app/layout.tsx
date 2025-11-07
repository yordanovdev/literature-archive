import type React from "react"
import type { Metadata } from "next"
import { Inter, Playfair_Display } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })
const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-serif" })

export const metadata: Metadata = {
  title: "Литературен Архив",
  description: "Съвременен помощник за изучаване на литература",
  keywords: ["литература", "анализ", "произведения", "автори", "теми", "мотиви", "български"],
  authors: [{ name: "Литературен Архив" }],
  creator: "Литературен Архив",
  openGraph: {
    type: "website",
    locale: "bg_BG",
    url: "https://literature-archive.vercel.app",
    title: "Литературен Архив",
    description: "Колекция от литературни произведения с подробен анализ",
    siteName: "Литературен Архив",
    images: [
      {
        url: "/icon.png",
        width: 1200,
        height: 630,
        alt: "Литературен Архив - Колекция от литературни произведения",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Литературен Архив",
    description: "Колекция от литературни произведения с подробен анализ",
    images: ["/icon.png"],
  },
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/icon.svg", type: "image/svg+xml" },
    ],
    apple: "/apple-icon.png",
  },
  generator: 'v0.app'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${playfair.variable}`}>{children}</body>
    </html>
  )
}
