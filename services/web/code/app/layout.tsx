import type React from "react"
import type { Metadata } from "next"
import { Inter, Manrope } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { MainLayout } from "@/components/layout/main-layout"
import { AuthProvider } from "@/components/providers/session-provider"

const inter = Inter({ subsets: ["latin"] })
const manrope = Manrope({ 
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-manrope"
})

export const metadata: Metadata = {
  title: "Kaleo - Nutrition Tracking",
  description: "Track your calories and nutrition with Kaleo",
  generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} ${manrope.variable} bg-background`}>
        <AuthProvider>
          <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false} disableTransitionOnChange>
            <MainLayout>{children}</MainLayout>
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
