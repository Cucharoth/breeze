'use client';

import { useTheme } from '@/components/ThemeContext';
import { Sparkles, Flame, PenLine, Trees, Tent, Scroll, BookOpen } from 'lucide-react';
import { LucideProps } from 'lucide-react';

interface ThemeIconProps extends LucideProps {
  type: 'creation' | 'action' | 'environment';
}

export function ThemeIcon({ type, ...props }: ThemeIconProps) {
  const { theme } = useTheme();

  if (type === 'creation') {
    switch (theme) {
      case 'obsidian': return <PenLine {...props} />;
      case 'glass': return <Sparkles {...props} />;
      case 'tavern': return <Scroll {...props} />;
      case 'campfire': return <Flame {...props} />;
      default: return <Sparkles {...props} />;
    }
  }

  if (type === 'action') {
    switch (theme) {
      case 'obsidian': return <Flame {...props} />;
      case 'glass': return <Sparkles {...props} />;
      case 'campfire': return <Tent {...props} />;
      default: return <Sparkles {...props} />;
    }
  }

  return <BookOpen {...props} />;
}
