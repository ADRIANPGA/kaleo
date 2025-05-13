"use client"

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "@/components/ui/chart"

const data = [
  { name: "Mon", calories: 1950 },
  { name: "Tue", calories: 2100 },
  { name: "Wed", calories: 1750 },
  { name: "Thu", calories: 2200 },
  { name: "Fri", calories: 1850 },
  { name: "Sat", calories: 2300 },
  { name: "Sun", calories: 1850 },
]

export function CalorieChart() {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12 }} />
          <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12 }} domain={[0, 2500]} tickCount={6} />
          <Tooltip
            cursor={{ fill: "rgba(0, 0, 0, 0.05)" }}
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                return (
                  <div className="rounded-lg border bg-background p-2 shadow-sm">
                    <div className="grid grid-cols-2 gap-2">
                      <div className="flex flex-col">
                        <span className="text-[0.70rem] uppercase text-muted-foreground">Day</span>
                        <span className="font-bold text-muted-foreground">{payload[0].payload.name}</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-[0.70rem] uppercase text-muted-foreground">Calories</span>
                        <span className="font-bold">{payload[0].value}</span>
                      </div>
                    </div>
                  </div>
                )
              }
              return null
            }}
          />
          <Bar dataKey="calories" fill="#22c55e" radius={[4, 4, 0, 0]} barSize={30} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
