"use client"

import { useEffect } from "react"
import { useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"

export default function AuthErrorPage() {
  const searchParams = useSearchParams()
  const error = searchParams.get("error")

  useEffect(() => {
    // Log the error for debugging
    console.error("Authentication error:", error)
  }, [error])

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-2 text-center">
          <CardTitle className="text-2xl font-semibold">Authentication Error</CardTitle>
          <CardDescription>
            {error === "AccessDenied"
              ? "You don't have permission to access this resource."
              : "An error occurred during authentication."}
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col items-center space-y-4">
          <Button asChild>
            <Link href="/">Return to Home</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/login">Try Again</Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  )
} 