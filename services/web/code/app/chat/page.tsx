import { ChatInterface } from "@/components/chat/chat-interface"

export default function ChatPage() {
  return (
    <div className="flex h-[calc(100vh-8rem)] flex-col">
      <div className="mb-4">
        <h1 className="text-3xl font-bold tracking-tight">Nutrition Coach</h1>
        <p className="text-muted-foreground">Chat with your personal nutrition coach</p>
      </div>
      <ChatInterface />
    </div>
  )
}
