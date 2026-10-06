# Dera Speaks

Website built with Vite, React, TypeScript and Tailwind CSS, hosted on Vercel, with Supabase as the backend.

## Local development

```bash
npm install
cp .env.example .env   # fill in the Supabase values
npm run dev
```

## Deploy

Vercel builds with `npm run build` and serves `dist/`. Set `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` in the Vercel project's environment variables.
