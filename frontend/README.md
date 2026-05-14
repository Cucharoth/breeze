# Breeze-RP Frontend

The frontend for Breeze-RP, a minimalist, privacy-first roleplay application. Built with Next.js 15, Tailwind CSS v4, and Zod.

## Prerequisites

- [Node.js 20+](https://nodejs.org/)
- [npm](https://www.npmjs.com/)

## Local Development

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Create a `.env.local` file in the `frontend/` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_IS_PROD=false
```

### 3. Run the Development Server
```bash
npm run dev
```
The application will be available at `http://localhost:3000`.

## Design System

- **Framework**: Next.js 15 (App Router)
- **Styling**: Tailwind CSS v4 (CSS-first configuration)
- **Design Aesthetic**: Dark Glassmorphism
- **Icons**: Lucide React
- **Typography**: Outfit (Sans), JetBrains Mono (Mono)

## Architecture

- **State Management**: React Hooks + Client Components
- **API Client**: Axios with global logging interceptors
- **Validation**: Zod schemas for all API payloads
- **Best Practices**: 
    - Next.js 15 Server/Client component boundaries
    - Zod-first validation logic
    - Centralized design tokens in `globals.css` using Tailwind v4 `@theme`

## Deployment

Build the production bundle:
```bash
npm run build
npm run start
```

For the entire stack (including backend):
```bash
docker-compose up --build
```
