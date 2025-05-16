"use client"

import { useState } from "react"
import { Plus, ChevronDown, ChevronUp } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import { cn } from "@/lib/utils"

// Helper to format date
const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

// Nutrition goals
const DAILY_GOALS = {
  calories: 2000,  // Standard 2000 calorie diet
  protein: 150,    // grams
  carbs: 250,      // grams
  fat: 65          // grams
}

const TODAY = new Date()
const YESTERDAY = new Date(TODAY)
YESTERDAY.setDate(YESTERDAY.getDate() - 1)

const DAILY_LOGS = [
  {
    date: TODAY,
    meals: [
      {
        id: 1,
        time: "8:30 AM",
        type: "Breakfast",
        items: [
          { name: "Oatmeal with Berries", calories: 280, protein: 8, carbs: 45, fat: 6 },
          { name: "Greek Yogurt", calories: 120, protein: 15, carbs: 8, fat: 0 },
          { name: "Black Coffee", calories: 5, protein: 0, carbs: 0, fat: 0 },
        ],
      },
      {
        id: 2,
        time: "11:00 AM",
        type: "Snack",
        items: [
          { name: "Apple", calories: 95, protein: 0, carbs: 25, fat: 0 },
          { name: "Almonds (1oz)", calories: 164, protein: 6, carbs: 6, fat: 14 },
        ],
      },
      {
        id: 3,
        time: "1:30 PM",
        type: "Lunch",
        items: [
          { name: "Grilled Chicken Salad", calories: 350, protein: 35, carbs: 15, fat: 18 },
          { name: "Whole Grain Bread", calories: 140, protein: 7, carbs: 28, fat: 2 },
          { name: "Olive Oil Dressing", calories: 120, protein: 0, carbs: 0, fat: 14 },
        ],
      },
      {
        id: 4,
        time: "4:00 PM",
        type: "Snack",
        items: [
          { name: "Protein Shake", calories: 160, protein: 25, carbs: 8, fat: 2 },
          { name: "Banana", calories: 105, protein: 1, carbs: 27, fat: 0 },
        ],
      },
      {
        id: 5,
        time: "7:00 PM",
        type: "Dinner",
        items: [
          { name: "Salmon Fillet", calories: 412, protein: 46, carbs: 0, fat: 28 },
          { name: "Brown Rice", calories: 216, protein: 5, carbs: 45, fat: 2 },
          { name: "Steamed Broccoli", calories: 55, protein: 4, carbs: 11, fat: 0 },
          { name: "Olive Oil", calories: 120, protein: 0, carbs: 0, fat: 14 },
        ],
      },
    ]
  },
  {
    date: YESTERDAY,
    meals: [
      {
        id: 1,
        time: "9:00 AM",
        type: "Breakfast",
        items: [
          { name: "Scrambled Eggs", calories: 210, protein: 14, carbs: 2, fat: 16 },
          { name: "Toast", calories: 80, protein: 3, carbs: 15, fat: 1 },
          { name: "Orange Juice", calories: 110, protein: 2, carbs: 26, fat: 0 },
        ],
      },
      {
        id: 2,
        time: "1:00 PM",
        type: "Lunch",
        items: [
          { name: "Turkey Sandwich", calories: 320, protein: 28, carbs: 38, fat: 8 },
          { name: "Mixed Salad", calories: 70, protein: 2, carbs: 14, fat: 1 },
        ],
      },
      {
        id: 3,
        time: "6:30 PM",
        type: "Dinner",
        items: [
          { name: "Grilled Steak", calories: 375, protein: 42, carbs: 0, fat: 22 },
          { name: "Sweet Potato", calories: 180, protein: 4, carbs: 41, fat: 0 },
          { name: "Green Beans", calories: 35, protein: 2, carbs: 7, fat: 0 },
        ],
      },
    ]
  }
]

export default function FoodLogPage() {
  const [dailyLogs, setDailyLogs] = useState(DAILY_LOGS)
  const [openDays, setOpenDays] = useState<Date[]>([TODAY])

  const getTotalNutrition = (items: typeof DAILY_LOGS[0]['meals'][0]['items']) => {
    return items.reduce((acc, item) => ({
      calories: acc.calories + item.calories,
      protein: acc.protein + item.protein,
      carbs: acc.carbs + item.carbs,
      fat: acc.fat + item.fat,
    }), { calories: 0, protein: 0, carbs: 0, fat: 0 })
  }

  const getDayTotal = (meals: typeof DAILY_LOGS[0]['meals']) => {
    return meals.reduce((acc, meal) => {
      const mealTotal = getTotalNutrition(meal.items)
      return {
        calories: acc.calories + mealTotal.calories,
        protein: acc.protein + mealTotal.protein,
        carbs: acc.carbs + mealTotal.carbs,
        fat: acc.fat + mealTotal.fat,
      }
    }, { calories: 0, protein: 0, carbs: 0, fat: 0 })
  }

  const toggleDay = (date: Date) => {
    setOpenDays(prev => {
      const isOpen = prev.some(d => d.getTime() === date.getTime())
      if (isOpen) {
        return prev.filter(d => d.getTime() !== date.getTime())
      } else {
        return [...prev, date]
      }
    })
  }

  const isDayOpen = (date: Date) => {
    return openDays.some(d => d.getTime() === date.getTime())
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Food Log</h2>
          <p className="text-muted-foreground">
            Track your meals and nutritional intake
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add Meal
        </Button>
      </div>

      <div className="space-y-6">
        {dailyLogs.map((dayLog) => {
          const dayTotal = getDayTotal(dayLog.meals)
          const isOpen = isDayOpen(dayLog.date)
          const hasReachedCalorieGoal = dayTotal.calories >= DAILY_GOALS.calories

          return (
            <Collapsible
              key={dayLog.date.toISOString()}
              open={isOpen}
              onOpenChange={() => toggleDay(dayLog.date)}
            >
              <Card>
                <CollapsibleTrigger asChild>
                  <CardHeader className="cursor-pointer hover:bg-muted/50">
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle>{formatDate(dayLog.date)}</CardTitle>
                        <CardDescription>
                          {dayLog.meals.length} meals • 
                          <span className={cn(
                            "ml-1",
                            hasReachedCalorieGoal && "text-green-500 font-medium"
                          )}>
                            {dayTotal.calories} calories
                          </span>
                          {hasReachedCalorieGoal && " 🎯"}
                        </CardDescription>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="hidden md:flex gap-4 text-sm text-muted-foreground">
                          <span>{dayTotal.protein}g protein</span>
                          <span>{dayTotal.carbs}g carbs</span>
                          <span>{dayTotal.fat}g fat</span>
                        </div>
                        {isOpen ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                      </div>
                    </div>
                  </CardHeader>
                </CollapsibleTrigger>
                
                <CollapsibleContent>
                  <CardContent className="pt-0">
                    <div className="space-y-4">
                      {dayLog.meals.map((meal) => {
                        const total = getTotalNutrition(meal.items)
                        return (
                          <Card key={meal.id}>
                            <CardHeader className="pb-4">
                              <div className="flex items-center justify-between">
                                <div>
                                  <CardTitle>{meal.type}</CardTitle>
                                  <CardDescription>{meal.time}</CardDescription>
                                </div>
                                <div className="flex gap-4 text-sm text-muted-foreground">
                                  <span className={cn(
                                    hasReachedCalorieGoal && "text-green-500"
                                  )}>{total.calories} cal</span>
                                  <span>{total.protein}g protein</span>
                                  <span>{total.carbs}g carbs</span>
                                  <span>{total.fat}g fat</span>
                                </div>
                              </div>
                            </CardHeader>
                            <CardContent>
                              <ul className="space-y-2">
                                {meal.items.map((item, index) => (
                                  <li key={index} className="flex items-center justify-between text-sm">
                                    <span>{item.name}</span>
                                    <div className="flex gap-4 text-muted-foreground">
                                      <span className={cn(
                                        hasReachedCalorieGoal && "text-green-500"
                                      )}>{item.calories} cal</span>
                                      <span>{item.protein}g protein</span>
                                      <span>{item.carbs}g carbs</span>
                                      <span>{item.fat}g fat</span>
                                    </div>
                                  </li>
                                ))}
                              </ul>
                            </CardContent>
                          </Card>
                        )
                      })}
                    </div>
                  </CardContent>
                </CollapsibleContent>
              </Card>
            </Collapsible>
          )
        })}
      </div>
    </div>
  )
} 