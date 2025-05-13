"use client"

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip, Legend } from "@/components/ui/chart"

const data = [
  { name: "Protein", value: 95, color: "#22c55e" },
  { name: "Carbs", value: 210, color: "#3b82f6" },
  { name: "Fat", value: 65, color: "#f59e0b" },
]

export function MacronutrientChart() {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={2} dataKey="value">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                return (
                  <div className="rounded-lg border bg-background p-2 shadow-sm">
                    <div className="grid grid-cols-2 gap-2">
                      <div className="flex flex-col">
                        <span className="text-[0.70rem] uppercase text-muted-foreground">Nutrient</span>
                        <span className="font-bold text-muted-foreground">{payload[0].name}</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-[0.70rem] uppercase text-muted-foreground">Amount</span>
                        <span className="font-bold">{payload[0].value}g</span>
                      </div>
                    </div>
                  </div>
                )
              }
              return null
            }}
          />
          <Legend layout="horizontal" verticalAlign="bottom" align="center" iconType="circle" iconSize={10} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
