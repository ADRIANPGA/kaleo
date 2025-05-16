"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useState, useEffect } from "react"
import { BarChart3, MessageSquare, Utensils, User, LogOut, Settings, Moon, Sun, Laptop } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu"
import { cn } from "@/lib/utils"
import { useTheme } from "next-themes"

const navigationItems = [
  {
    title: "See",
    icon: BarChart3,
    items: [
      {
        title: "Dashboard",
        description: "View your nutrition overview",
        href: "/dashboard",
        icon: BarChart3,
      },
      {
        title: "Reports",
        description: "Analyze your nutrition trends",
        href: "/reports",
        icon: BarChart3,
      },
    ],
  },
  {
    title: "Eat",
    icon: Utensils,
    items: [
      {
        title: "Diet",
        description: "View your meal plans",
        href: "/diet",
        icon: Utensils,
      },
      {
        title: "Food Log",
        description: "Log your daily meals",
        href: "/food-log",
        icon: Utensils,
      },
    ],
  },
  {
    title: "Chat",
    icon: MessageSquare,
    items: [
      {
        title: "Nutrition Coach",
        description: "Chat with your nutrition coach",
        href: "/chat",
        icon: MessageSquare,
      },
    ],
  },
]

export function Header() {
  const pathname = usePathname()
  const [activeItem, setActiveItem] = useState("")
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const ThemeIcon = mounted ? (
    theme === "dark" ? <Moon className="h-5 w-5" /> : 
    theme === "light" ? <Sun className="h-5 w-5" /> : 
    <Laptop className="h-5 w-5" />
  ) : (
    <Sun className="h-5 w-5" />
  )

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center px-6">
        <div className="flex items-center gap-4 md:gap-8">
          <Link href="/" className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-green-400 to-green-600"></div>
            <span className="font-bold text-lg hidden sm:inline">Kaleo</span>
          </Link>
        </div>

        <NavigationMenu className="mx-auto hidden md:flex">
          <NavigationMenuList>
            {navigationItems.map((item) => (
              <NavigationMenuItem key={item.title}>
                <NavigationMenuTrigger
                  className={cn("text-base font-medium", activeItem === item.title && "text-primary")}
                  onClick={() => setActiveItem(item.title)}
                >
                  {item.title}
                </NavigationMenuTrigger>
                <NavigationMenuContent>
                  <ul className="grid w-[400px] gap-3 p-4 md:w-[500px] md:grid-cols-2 lg:w-[600px]">
                    {item.items.map((subItem) => (
                      <li key={subItem.title}>
                        <NavigationMenuLink asChild>
                          <Link
                            href={subItem.href}
                            className={cn(
                              "block select-none space-y-1 rounded-2xl p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
                              pathname === subItem.href && "bg-accent",
                            )}
                          >
                            <div className="flex items-center gap-2">
                              <subItem.icon className="h-4 w-4" />
                              <div className="text-sm font-medium leading-none">{subItem.title}</div>
                            </div>
                            <p className="line-clamp-2 text-sm leading-snug text-muted-foreground">
                              {subItem.description}
                            </p>
                          </Link>
                        </NavigationMenuLink>
                      </li>
                    ))}
                  </ul>
                </NavigationMenuContent>
              </NavigationMenuItem>
            ))}
          </NavigationMenuList>
        </NavigationMenu>

        <div className="flex items-center gap-4 ml-auto">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                {ThemeIcon}
                <span className="sr-only">Toggle theme</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setTheme("light")}> <Sun className="mr-2 h-4 w-4" /> Light </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setTheme("dark")}> <Moon className="mr-2 h-4 w-4" /> Dark </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setTheme("system")}> <Laptop className="mr-2 h-4 w-4" /> System </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                <Avatar className="h-8 w-8">
                  <AvatarImage src="/placeholder.svg?height=32&width=32" alt="User" />
                  <AvatarFallback>JD</AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end" forceMount>
              <DropdownMenuLabel className="font-normal">
                <div className="flex flex-col space-y-1">
                  <p className="text-sm font-medium leading-none">John Doe</p>
                  <p className="text-xs leading-none text-muted-foreground">john.doe@example.com</p>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <User className="mr-2 h-4 w-4" />
                <span>Profile</span>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" />
                <span>Settings</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <LogOut className="mr-2 h-4 w-4" />
                <span>Log out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}
