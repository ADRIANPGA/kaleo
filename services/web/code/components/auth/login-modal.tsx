import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Chrome } from "lucide-react"
import { signIn } from "next-auth/react"
import { useRouter } from "next/navigation"

interface LoginModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

export function LoginModal({ isOpen, onClose, onSuccess }: LoginModalProps) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)
    try {
      const result = await signIn("azure-ad", {
        email,
        password,
        redirect: false,
      })

      if (result?.error) {
        setError(result.error)
      } else {
        onSuccess()
      }
    } catch (error) {
      setError("An error occurred during sign in")
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleMicrosoftLogin = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const result = await signIn("azure-ad", {
        redirect: false,
      })
      
      if (result?.error) {
        setError(result.error)
      } else if (result?.url) {
        // Redirect to the Microsoft login page
        router.push(result.url)
      }
    } catch (error) {
      setError("An error occurred during Microsoft sign in")
      console.error(error)
      setIsLoading(false)
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <Card className="border-0 shadow-none">
          <CardHeader className="space-y-2 text-center">
            <div className="mx-auto h-12 w-12 rounded-full bg-gradient-to-br from-green-400 to-green-600"></div>
            <CardTitle className="text-2xl font-semibold">Welcome to Kaleo</CardTitle>
            <CardDescription>Sign in to continue to your nutrition journey</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
                {error}
              </div>
            )}
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input 
                  id="email" 
                  type="email" 
                  placeholder="Enter your email" 
                  required 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input 
                  id="password" 
                  type="password" 
                  placeholder="Enter your password" 
                  required 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "Signing in..." : "Sign in"}
              </Button>
            </form>
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">Or continue with</span>
              </div>
            </div>
            <Button 
              variant="outline" 
              className="w-full justify-start gap-2" 
              disabled={isLoading}
              onClick={handleMicrosoftLogin}
            >
              <Chrome className="h-5 w-5" />
              Sign in with Microsoft
            </Button>
          </CardContent>
        </Card>
      </DialogContent>
    </Dialog>
  )
} 