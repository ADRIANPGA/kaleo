"use client"

import { useEffect, useRef, useState } from "react"
import { Input } from "@/components/ui/input"
import { useRouter } from "next/navigation"
import { LoginModal } from "@/components/auth/login-modal"

// Expanded food emoji set
const foodEmojis = [
  "🍎", "🍕", "🥦", "🍔", "🍣", "🍩", "🍇", "🍟", "🥑", "🍉", "🍌", "🍒", "🍪", "🍓", "🍊", "🍋", "🍈", "🍍", "🍔", "🥨", "🥕", "🍜", "🍚", "🍞", "🥐", "🍦", "🍤", "🍿", "🍫", "🍬", "🍭", "🍯", "🥓", "🥚", "🍔", "🍗", "🍖", "🍛", "🍱", "🍲", "🍥", "🍧", "🍨", "🍰", "🍮", "🍢", "🍡", "🍧", "🍠", "🥟", "🥠", "🥡", "🥙", "🥗", "🥪", "🥫", "🥞", "🧇", "🧀", "🍖", "🍤", "🍣", "🍥", "🍡", "🍢", "🍧", "🍨", "🍦", "🍰", "🍮", "🍫", "🍬", "🍭", "🍯"
];
const words = ["EAT", "TRACK", "SUCCESS", "PLAN", "HEALTH", "ACHIEVE GOALS", "FUEL OUR LIFE", "GROW", "FOCUS", "LIVE"];

function getRandom(min: number, max: number) {
  return Math.random() * (max - min) + min;
}

function getEmojiCount() {
  if (typeof window === "undefined") return 12;
  const width = window.innerWidth;
  if (width < 640) return 8;
  if (width < 1024) return 16;
  return 24;
}

function getRandomEmoji() {
  return foodEmojis[Math.floor(Math.random() * foodEmojis.length)];
}

function useFloatingEmojis() {
  const [emojis, setEmojis] = useState<Array<{
    emoji: string;
    x: number;
    y: number;
    speedX: number;
    speedY: number;
    size: number;
  }>>([]);

  // Initialize emojis only on client side
  useEffect(() => {
    const count = getEmojiCount();
    setEmojis(Array.from({ length: count }, () => createEmojiConfig()));
  }, []);

  // Recalculate emoji count on resize
  useEffect(() => {
    if (emojis.length === 0) return; // Skip if not initialized yet

    function handleResize() {
      setEmojis((prev) => {
        const count = getEmojiCount();
        if (prev.length === count) return prev;
        if (prev.length < count) {
          return [
            ...prev,
            ...Array.from({ length: count - prev.length }, () => createEmojiConfig())
          ];
        }
        return prev.slice(0, count);
      });
    }
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [emojis.length]);

  // Animate emojis
  useEffect(() => {
    if (emojis.length === 0) return; // Skip if not initialized yet

    let raf: number;
    function animate() {
      setEmojis((prev) =>
        prev.map((cfg) => {
          let { x, y, speedX, speedY, emoji, size } = cfg;
          x += speedX;
          y += speedY;
          // If out of bounds, respawn
          if (x < -10 || x > 110 || y < -10 || y > 110) {
            // Respawn at a random edge
            const edge = Math.floor(Math.random() * 4);
            if (edge === 0) { // left
              x = -10; y = getRandom(0, 100);
              speedX = getRandom(0.1, 0.5); speedY = getRandom(-0.1, 0.1);
            } else if (edge === 1) { // right
              x = 110; y = getRandom(0, 100);
              speedX = -getRandom(0.1, 0.5); speedY = getRandom(-0.1, 0.1);
            } else if (edge === 2) { // top
              x = getRandom(0, 100); y = -10;
              speedX = getRandom(-0.1, 0.1); speedY = getRandom(0.1, 0.5);
            } else { // bottom
              x = getRandom(0, 100); y = 110;
              speedX = getRandom(-0.1, 0.1); speedY = -getRandom(0.1, 0.5);
            }
            emoji = getRandomEmoji();
            size = getRandom(2.5, 4.5);
          }
          return { ...cfg, x, y, speedX, speedY, emoji, size };
        })
      );
      raf = requestAnimationFrame(animate);
    }
    raf = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(raf);
  }, [emojis.length]);

  return emojis;
}

function createEmojiConfig() {
  // Start at a random edge
  const edge = Math.floor(Math.random() * 4);
  let x, y, speedX, speedY;
  if (edge === 0) { // left
    x = -10; y = getRandom(0, 100);
    speedX = getRandom(0.1, 0.5); speedY = getRandom(-0.1, 0.1);
  } else if (edge === 1) { // right
    x = 110; y = getRandom(0, 100);
    speedX = -getRandom(0.1, 0.5); speedY = getRandom(-0.1, 0.1);
  } else if (edge === 2) { // top
    x = getRandom(0, 100); y = -10;
    speedX = getRandom(-0.1, 0.1); speedY = getRandom(0.1, 0.5);
  } else { // bottom
    x = getRandom(0, 100); y = 110;
    speedX = getRandom(-0.1, 0.1); speedY = -getRandom(0.1, 0.5);
  }
  return {
    emoji: getRandomEmoji(),
    x,
    y,
    speedX,
    speedY,
    size: getRandom(2.5, 4.5),
  };
}

export default function LandingPage() {
  const router = useRouter();
  const [index, setIndex] = useState(0);
  const [display, setDisplay] = useState("");
  const [typing, setTyping] = useState(true);
  const [charIndex, setCharIndex] = useState(0);
  const [deleting, setDeleting] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [pendingMessage, setPendingMessage] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Floating emojis
  const emojis = useFloatingEmojis();

  // Function to get next random index different from previous
  const getNextRandomIndex = (currentIndex: number) => {
    if (words.length <= 1) return 0;
    const availableIndices = words
      .map((_, i) => i)
      .filter(i => i !== currentIndex);
    return availableIndices[Math.floor(Math.random() * availableIndices.length)];
  };

  // Typewriter logic
  useEffect(() => {
    let timeout: NodeJS.Timeout;
    if (typing) {
      if (!deleting) {
        if (charIndex < words[index].length) {
          setDisplay(words[index].slice(0, charIndex + 1));
          timeout = setTimeout(() => setCharIndex((c) => c + 1), 120);
        } else {
          timeout = setTimeout(() => setDeleting(true), 1200);
        }
      } else {
        if (charIndex > 0) {
          setDisplay(words[index].slice(0, charIndex - 1));
          timeout = setTimeout(() => setCharIndex((c) => c - 1), 60);
        } else {
          setDeleting(false);
          const nextIndex = getNextRandomIndex(index);
          setIndex(nextIndex);
          setCharIndex(0);
          timeout = setTimeout(() => setTyping(true), 400);
        }
      }
    } else {
      setDisplay("");
      setCharIndex(0);
      timeout = setTimeout(() => setTyping(true), 1000);
    }
    return () => clearTimeout(timeout);
  }, [typing, charIndex, deleting, index]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const input = inputRef.current?.value.trim();
    if (input) {
      setPendingMessage(input);
      setShowLoginModal(true);
    }
  };

  const handleLoginSuccess = () => {
    setShowLoginModal(false);
    if (pendingMessage) {
      router.push(`/chat?message=${encodeURIComponent(pendingMessage)}`);
      setPendingMessage(null);
    }
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center bg-background overflow-hidden">
      {/* Floating food emojis */}
      <div className="absolute inset-0 w-full h-full pointer-events-none select-none z-0">
        {emojis.map((cfg, i) => (
          <span
            key={i}
            style={{
              left: `${cfg.x}%`,
              top: `${cfg.y}%`,
              fontSize: `${cfg.size}rem`,
              position: "absolute",
              willChange: "transform, left, top",
              userSelect: "none",
            }}
          >
            {cfg.emoji}
          </span>
        ))}
      </div>
      {/* Foreground content */}
      <div className="relative z-10 flex flex-col items-center justify-center w-full">
        <h1 className="text-6xl md:text-8xl font-bold text-foreground mb-6 tracking-[-0.02em] text-center font-[var(--font-manrope)]">
          WELCOME TO KALEO
        </h1>
        <div className="text-3xl md:text-5xl font-medium h-20 text-center mb-4">
          <span className="text-foreground">LET'S </span>
          <span className="text-primary">{display}</span>
        </div>
        <form
          className="w-full max-w-md mt-2"
          onSubmit={handleSubmit}
        >
          <Input
            ref={inputRef}
            type="text"
            placeholder="Start typing to chat..."
            className="bg-transparent/5 border-0 placeholder:text-muted-foreground/50 text-foreground shadow-none focus:ring-0 backdrop-blur-sm text-center rounded-full px-6 py-6 text-lg"
            autoFocus
          />
        </form>
      </div>

      <LoginModal 
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onSuccess={handleLoginSuccess}
      />
    </div>
  );
}

import { BarChart3, MessageSquare, Utensils } from "lucide-react"
