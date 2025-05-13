"use client"

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

const dietPlan = [
  {
    id: "breakfast",
    title: "Breakfast",
    calories: 520,
    time: "7:00 - 8:30 AM",
    foods: [
      { name: "Oatmeal with almond milk", portion: "1 cup", calories: 300, macros: { protein: 10, carbs: 50, fat: 7 } },
      { name: "Blueberries", portion: "1/2 cup", calories: 40, macros: { protein: 0, carbs: 10, fat: 0 } },
      { name: "Scrambled eggs", portion: "2 eggs", calories: 180, macros: { protein: 12, carbs: 0, fat: 14 } },
    ],
  },
  {
    id: "morning-snack",
    title: "Morning Snack",
    calories: 200,
    time: "10:00 - 11:00 AM",
    foods: [
      { name: "Greek yogurt", portion: "1 cup", calories: 150, macros: { protein: 20, carbs: 8, fat: 0 } },
      { name: "Almonds", portion: "10 almonds", calories: 70, macros: { protein: 3, carbs: 2, fat: 6 } },
    ],
  },
  {
    id: "lunch",
    title: "Lunch",
    calories: 650,
    time: "12:30 - 1:30 PM",
    foods: [
      { name: "Grilled chicken breast", portion: "5 oz", calories: 250, macros: { protein: 35, carbs: 0, fat: 10 } },
      { name: "Quinoa", portion: "1/2 cup", calories: 120, macros: { protein: 4, carbs: 20, fat: 2 } },
      { name: "Mixed vegetables", portion: "1 cup", calories: 80, macros: { protein: 2, carbs: 15, fat: 0 } },
      { name: "Olive oil dressing", portion: "1 tbsp", calories: 120, macros: { protein: 0, carbs: 0, fat: 14 } },
    ],
  },
  {
    id: "afternoon-snack",
    title: "Afternoon Snack",
    calories: 180,
    time: "3:30 - 4:30 PM",
    foods: [
      { name: "Apple", portion: "1 medium", calories: 80, macros: { protein: 0, carbs: 20, fat: 0 } },
      { name: "Peanut butter", portion: "1 tbsp", calories: 100, macros: { protein: 4, carbs: 3, fat: 8 } },
    ],
  },
  {
    id: "dinner",
    title: "Dinner",
    calories: 580,
    time: "6:30 - 7:30 PM",
    foods: [
      { name: "Baked salmon", portion: "5 oz", calories: 300, macros: { protein: 30, carbs: 0, fat: 18 } },
      { name: "Brown rice", portion: "1/2 cup", calories: 110, macros: { protein: 2, carbs: 22, fat: 1 } },
      { name: "Steamed broccoli", portion: "1 cup", calories: 50, macros: { protein: 3, carbs: 10, fat: 0 } },
      { name: "Avocado", portion: "1/4", calories: 80, macros: { protein: 1, carbs: 4, fat: 7 } },
    ],
  },
  {
    id: "evening-snack",
    title: "Evening Snack (Optional)",
    calories: 120,
    time: "8:30 - 9:30 PM",
    foods: [
      { name: "Cottage cheese", portion: "1/2 cup", calories: 90, macros: { protein: 14, carbs: 3, fat: 2 } },
      { name: "Cinnamon", portion: "1/4 tsp", calories: 0, macros: { protein: 0, carbs: 0, fat: 0 } },
      { name: "Honey", portion: "1 tsp", calories: 30, macros: { protein: 0, carbs: 8, fat: 0 } },
    ],
  },
]

export function DietPlan() {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold">Your Daily Meal Plan</h2>
            <p className="text-sm text-muted-foreground">2,250 calories • 130g protein • 220g carbs • 85g fat</p>
          </div>
          <div className="flex gap-2">
            <Badge variant="outline">High Protein</Badge>
            <Badge variant="outline">Balanced</Badge>
          </div>
        </div>

        <Accordion type="single" collapsible className="w-full">
          {dietPlan.map((meal) => (
            <AccordionItem key={meal.id} value={meal.id}>
              <AccordionTrigger className="py-4">
                <div className="flex flex-1 items-center justify-between pr-4">
                  <div className="text-left">
                    <div className="font-medium">{meal.title}</div>
                    <div className="text-sm text-muted-foreground">{meal.time}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">{meal.calories} kcal</div>
                    <div className="text-sm text-muted-foreground">{meal.foods.length} items</div>
                  </div>
                </div>
              </AccordionTrigger>
              <AccordionContent>
                <div className="space-y-4 px-1 pb-4">
                  {meal.foods.map((food, index) => (
                    <div key={index} className="flex items-center justify-between rounded-2xl bg-accent/50 p-3">
                      <div>
                        <div className="font-medium">{food.name}</div>
                        <div className="text-sm text-muted-foreground">{food.portion}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-medium">{food.calories} kcal</div>
                        <div className="text-xs text-muted-foreground">
                          P: {food.macros.protein}g • C: {food.macros.carbs}g • F: {food.macros.fat}g
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </CardContent>
    </Card>
  )
}
