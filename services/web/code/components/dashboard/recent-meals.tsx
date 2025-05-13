"use client"

import { Apple, Coffee, Egg, Salad, UtensilsCrossed } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

const meals = [
  {
    id: 1,
    name: "Breakfast",
    time: "8:30 AM",
    foods: [
      { name: "Oatmeal with berries", calories: 320, icon: Egg },
      { name: "Coffee with almond milk", calories: 40, icon: Coffee },
    ],
  },
  {
    id: 2,
    name: "Lunch",
    time: "12:45 PM",
    foods: [
      { name: "Grilled chicken salad", calories: 450, icon: Salad },
      { name: "Apple", calories: 80, icon: Apple },
    ],
  },
  {
    id: 3,
    name: "Dinner",
    time: "7:15 PM",
    foods: [
      { name: "Salmon with quinoa", calories: 520, icon: UtensilsCrossed },
      { name: "Steamed vegetables", calories: 120, icon: Salad },
    ],
  },
]

export function RecentMeals() {
  return (
    <TooltipProvider>
      <div className="space-y-6">
        {meals.map((meal) => (
          <div key={meal.id} className="space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="font-medium">{meal.name}</h3>
              <Tooltip>
                <TooltipTrigger asChild>
                  <span className="text-sm text-muted-foreground cursor-default">{meal.time}</span>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Logged at {meal.time}</p>
                </TooltipContent>
              </Tooltip>
            </div>
            <div className="space-y-2">
              {meal.foods.map((food, index) => (
                <div key={index} className="flex items-center justify-between rounded-2xl bg-accent/50 p-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-background">
                      <food.icon className="h-4 w-4" />
                    </div>
                    <span>{food.name}</span>
                  </div>
                  <span className="text-sm font-medium">{food.calories} kcal</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </TooltipProvider>
  )
}
