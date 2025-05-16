"use client"

import { useState } from "react"
import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ChatMessage } from "./chat-message"

type Message = {
  id: number;
  role: "assistant" | "user";
  content: string;
  timestamp: string;
}

// Mock chat data
const initialMessages: Message[] = [
  {
    id: 1,
    role: "assistant",
    content: "Hello! I'm your Kaleo nutrition coach. How can I help you today?",
    timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
  },
  {
    id: 2,
    role: "user",
    content: "I'm trying to increase my protein intake. Any suggestions?",
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
  },
  {
    id: 3,
    role: "assistant",
    content:
      "Great goal! Here are some high-protein foods you could add to your diet:\n\n" +
      "- **Lean meats**: Chicken breast, turkey, lean beef\n" +
      "- **Fish**: Salmon, tuna, tilapia\n" +
      "- **Plant-based**: Tofu, tempeh, legumes, quinoa\n" +
      "- **Dairy**: Greek yogurt, cottage cheese\n" +
      "- **Other**: Eggs, protein powder\n\n" +
      "Try to include a protein source with each meal. Would you like me to suggest some specific high-protein meal ideas?",
    timestamp: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
  },
]

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>(initialMessages)
  const [input, setInput] = useState("")

  const handleSendMessage = () => {
    if (!input.trim()) return

    // Add user message
    const userMessage: Message = {
      id: messages.length + 1,
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    }

    setMessages([...messages, userMessage])
    setInput("")

    // Simulate assistant response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: messages.length + 2,
        role: "assistant",
        content:
          "I'll help you with that! Let me provide some personalized advice based on your nutrition goals and preferences.",
        timestamp: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    }, 1000)
  }

  return (
    <div className="flex h-full flex-col rounded-2xl border bg-background shadow-sm">
      <ScrollArea className="flex-1 p-4">
        <div className="flex flex-col gap-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
        </div>
      </ScrollArea>
      <div className="border-t p-4">
        <form
          onSubmit={(e) => {
            e.preventDefault()
            handleSendMessage()
          }}
          className="flex items-center gap-2"
        >
          <Input
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1"
          />
          <Button type="submit" size="icon">
            <Send className="h-4 w-4" />
            <span className="sr-only">Send message</span>
          </Button>
        </form>
      </div>
    </div>
  )
}
