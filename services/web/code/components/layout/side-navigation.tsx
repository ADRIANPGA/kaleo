"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { BarChart3, MessageSquare, Utensils, Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { cn } from "@/lib/utils"
import { useIsMobile } from "@/hooks/use-mobile"

const navigationItems = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: BarChart3,
  },
  {
    title: "Chat",
    href: "/chat",
    icon: MessageSquare,
  },
  {
    title: "Diet",
    href: "/diet",
    icon: Utensils,
  },
]

export function SideNavigation() {
  const pathname = usePathname()
  const isMobile = useIsMobile()

  if (isMobile) {
    return (
      <Sheet>
        <SheetTrigger asChild>
          <Button
            variant="outline"
            size="icon"
            className="fixed bottom-4 right-4 z-40 h-12 w-12 rounded-full shadow-lg md:hidden"
          >
            <Menu className="h-6 w-6" />
            <span className="sr-only">Toggle navigation menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 p-0">
          <nav className="flex flex-col gap-2 p-4">
            {navigationItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-2xl px-3 py-2 text-sm font-medium transition-colors hover:bg-accent",
                  pathname === item.href ? "bg-accent" : "transparent",
                )}
              >
                <item.icon className="h-5 w-5" />
                {item.title}
              </Link>
            ))}
          </nav>
        </SheetContent>
      </Sheet>
    )
  }

  return (
    <div className="hidden w-64 flex-col border-r bg-background p-4 md:flex">
      <nav className="flex flex-col gap-2 pt-16">
        {navigationItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center gap-3 rounded-2xl px-3 py-2 text-sm font-medium transition-colors hover:bg-accent",
              pathname === item.href ? "bg-accent" : "transparent",
            )}
          >
            <item.icon className="h-5 w-5" />
            {item.title}
          </Link>
        ))}
      </nav>
    </div>
  )
}
