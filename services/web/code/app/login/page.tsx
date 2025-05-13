import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Chrome, Computer } from "lucide-react"

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-md shadow-sm">
        <CardHeader className="space-y-2 text-center">
          <div className="mx-auto h-12 w-12 rounded-full bg-gradient-to-br from-green-400 to-green-600"></div>
          <CardTitle className="text-2xl font-semibold">Welcome to Kaleo</CardTitle>
          <CardDescription>Enter the dashboard to track your nutrition and reach your health goals</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button className="w-full justify-start gap-2" asChild>
            <Link href="/dashboard">
              <Computer className="h-5 w-5" />
              Enter Dashboard
            </Link>
          </Button>
          <div className="text-center text-sm text-muted-foreground">
            By continuing, you agree to our{" "}
            <Link href="#" className="underline underline-offset-4 hover:text-primary">
              Terms of Service
            </Link>{" "}
            and{" "}
            <Link href="#" className="underline underline-offset-4 hover:text-primary">
              Privacy Policy
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
