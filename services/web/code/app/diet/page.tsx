import { DietPlan } from "@/components/diet/diet-plan"

export default function DietPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Diet Plan</h1>
        <p className="text-muted-foreground">Your personalized nutrition plan based on your goals</p>
      </div>
      <DietPlan />
    </div>
  )
}
