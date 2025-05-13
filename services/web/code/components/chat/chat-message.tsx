"use client"

import { format } from "date-fns"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"

interface ChatMessageProps {
  message: {
    id: number
    role: "user" | "assistant"
    content: string
    timestamp: string
  }
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user"
  const formattedTime = format(new Date(message.timestamp), "h:mm a")

  return (
    <TooltipProvider>
      <div className={cn("flex", isUser ? "justify-end" : "justify-start")}>
        <Tooltip>
          <TooltipTrigger asChild>
            <div
              className={cn(
                "max-w-[80%] rounded-2xl px-4 py-2",
                isUser ? "bg-primary text-primary-foreground" : "bg-accent text-accent-foreground",
              )}
            >
              <div className={cn("prose prose-sm max-w-none", isUser ? "prose-invert" : "")}>
                {message.content.split("\n").map((line, i) => (
                  <p key={i} className={line.startsWith("-") ? "my-0" : ""}>
                    {line}
                  </p>
                ))}
              </div>
            </div>
          </TooltipTrigger>
          <TooltipContent side={isUser ? "left" : "right"}>{formattedTime}</TooltipContent>
        </Tooltip>
      </div>
    </TooltipProvider>
  )
}
