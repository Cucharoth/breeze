<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Agent Development Guidelines: Frontend

This document outlines the established development practices, architecture, and UI conventions for the Breeze-RP frontend. Any AI agent modifying this codebase MUST adhere to these rules.

## Tech Stack & Core Next.js Practices
- **Framework**: Next.js (App Router, Node.js runtime preferred)
- **Styling**: Tailwind CSS v4
- **Language**: TypeScript
- **Validation**: Zod (for strict schema validation, type inference via `z.infer`, and safe API parsing via `safeParse`).
- **RSC Boundaries**: Default to Server Components. Add `'use client'` ONLY to the leaf components that require interactivity (hooks like `useState`, `onClick` handlers).
- **Async APIs (Next 15+)**: Remember that `params`, `searchParams`, `cookies()`, and `headers()` are asynchronous and must be awaited.
- **Images**: ALWAYS use `next/image` (`<Image />`) instead of standard `<img>` tags for automatic optimization.

## UI & Aesthetics (CRITICAL)
- **Semantic CSS**: Do NOT use raw Tailwind classes for primary structural styling (e.g., avoid hardcoding `bg-stone-900 border-amber-900/50`). 
- **The Design System**: Always use the semantic classes defined in `src/app/globals.css`. 
  - `.breeze-surface`: For main containers, cards, and forms. Handles backgrounds, borders, and glows based on the active theme.
  - `.breeze-input`: For text areas and inputs.
  - `.breeze-btn-primary`, `.breeze-btn-ghost`: For buttons.
- **Theme-Agnostic React**: React components should not contain `if (theme === 'obsidian')` logic for styling. The CSS custom properties and pseudo-elements in `globals.css` handle theme switching automatically via the `[data-theme]` attribute on the root html.

## Notifications & Feedback
- **Library**: `sonner`
- **Usage**: Use `toast.success()`, `toast.error()`, and `toast.loading()` for user-facing feedback during asynchronous actions. 
- **Placement**: Do not reinvent toast logic; `Toaster` is already globally mounted in `RootLayout`.

## Logging
- **Library**: Custom wrapper around `console` in `src/lib/logger.ts`
- **Rule**: Avoid leaving loose `console.log` statements. Use `logger.debug()`, `logger.info()`, or `logger.error()` for development state tracking.

## Architecture & Data Flow
- **Feature-Sliced Design**: Code is organized by feature in `src/features/` (e.g., `scenarios`, `stories`).
- **Hooks**: Data fetching and mutation should be wrapped in custom hooks (e.g., `useCreateScenario`).
  - Hooks must manage their own `isLoading` and `error` states.
  - Hooks are responsible for triggering `toast` notifications on success/failure.
  - Components should remain as "dumb" as possible, calling hook methods.
