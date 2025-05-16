import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { CalorieChart } from "@/components/dashboard/calorie-chart"
import { MacronutrientChart } from "@/components/dashboard/macronutrient-chart"
import { RecentMeals } from "@/components/dashboard/recent-meals"

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">Track your nutrition and reach your health goals</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base">Calories Today</CardTitle>
            <CardDescription>1,850 / 2,000 kcal</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">1,850</div>
            <Progress value={84} className="mt-2 h-2" />
            <p className="mt-2 text-xs text-muted-foreground">350 kcal remaining for today</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base">Protein</CardTitle>
            <CardDescription>95g / 120g</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">95g</div>
            <Progress value={79} className="mt-2 h-2" />
            <p className="mt-2 text-xs text-muted-foreground">25g remaining for today</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base">Water</CardTitle>
            <CardDescription>1.8L / 2.5L</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">1.8L</div>
            <Progress value={72} className="mt-2 h-2" />
            <p className="mt-2 text-xs text-muted-foreground">0.7L remaining for today</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Macronutrient Split</CardTitle>
            <CardDescription>Your macronutrient distribution for today</CardDescription>
          </CardHeader>
          <CardContent>
            <MacronutrientChart />
          </CardContent>
        </Card>
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Calorie Trend</CardTitle>
            <CardDescription>Your calorie intake over the last 7 days</CardDescription>
          </CardHeader>
          <CardContent>
            <CalorieChart />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Meals</CardTitle>
          <CardDescription>Your most recent logged meals</CardDescription>
        </CardHeader>
        <CardContent>
          <RecentMeals />
        </CardContent>
      </Card>
    </div>
  )
}
