"use client"

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { Flag } from "lucide-react"

const CALORIE_GOAL = 2000

const CustomBarLabel = (props: any) => {
  const { x, y, width, value } = props;
  if (value >= CALORIE_GOAL) {
    return (
      <g transform={`translate(${x + width/2 - 12},${y - 25})`}>
        <rect width="24" height="24" fill="none" />
        <path 
          d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z M4 22v-7" 
          stroke="currentColor" 
          strokeWidth="2" 
          strokeLinecap="round" 
          strokeLinejoin="round"
          className="text-primary"
        />
      </g>
    );
  }
  return null;
};

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
        <BarChart data={data} margin={{ top: 25, right: 5, left: 5, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12 }} />
          <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12 }} domain={[0, 2500]} tickCount={6} />
          <Tooltip
            cursor={{ fill: "rgba(0, 0, 0, 0.05)" }}
            content={(props) => {
              if (props.active && props.payload?.[0]) {
                const data = props.payload[0].payload;
                return (
                  <div className="rounded-lg border bg-background p-2 shadow-sm">
                    <div className="grid grid-cols-2 gap-2">
                      <div className="flex flex-col">
                        <span className="text-[0.70rem] uppercase text-muted-foreground">Day</span>
                        <span className="font-bold text-muted-foreground">{data.name}</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-[0.70rem] uppercase text-muted-foreground">Calories</span>
                        <span className="font-bold">{data.calories}</span>
                      </div>
                    </div>
                  </div>
                )
              }
              return null
            }}
          />
          <Bar 
            dataKey="calories" 
            fill="#22c55e" 
            radius={[4, 4, 0, 0]} 
            barSize={30}
            label={<CustomBarLabel />}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
