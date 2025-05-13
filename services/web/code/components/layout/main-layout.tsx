"use client"

import type React from "react"

import { usePathname } from "next/navigation"
import { Header } from "./header"
import { SideNavigation } from "./side-navigation"

export function MainLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

  // Don't show layout on landing page or login page
  if (pathname === "/" || pathname === "/login") {
    return <>{children}</>
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <div className="flex flex-1 pt-16">
        <SideNavigation />
        <main className="flex-1 p-6 md:p-8 max-w-7xl mx-auto w-full">{children}</main>
      </div>
    </div>
  )
}
