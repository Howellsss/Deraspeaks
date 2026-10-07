# Dera Speaks

The current site is the approved design mockup in `site/`: one HTML page (`site/index.html`) with its photos and videos in `site/img/`. Vercel copies `site/` into `dist/` and serves it as a static site (see `vercel.json`); there is nothing to install or compile.

## Preview locally

```bash
cd site && python3 -m http.server 8000
```

Then open http://localhost:8000.

## Next step

The Vite + React + TypeScript + Tailwind starter in `src/` (with the Supabase client) is kept for the full build: working booking form and newsletter, one address per page, and compressed images. Once that build is ready, `vercel.json` goes back to `npm run build` serving `dist/`, with `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` set in the Vercel project's environment variables.

## Deploying

Every push to `main` deploys to production. In Vercel, **Redeploy** rebuilds the same commit as the deployment you picked, so it will not pick up newer commits. If a push does not show up in Vercel's Deployments list, push again or use **Create Deployment** with the `main` branch.
