import { createClient } from '@supabase/supabase-js'

const url = import.meta.env.VITE_SUPABASE_URL as string | undefined
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined

// Null until the Supabase env vars are set (locally in .env, or in Vercel).
export const supabase = url && anonKey ? createClient(url, anonKey) : null
