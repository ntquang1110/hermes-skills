# Supabase / PostgREST — Relationship Resolution Debugging

## Symptom

An API query that joins two tables via a nested `select` returns an error:

```
{"code":"PGRST200","details":"Searched for a foreign key relationship between 'table_a' and 'table_b' in the schema 'public', but no matches were found.","hint":"Perhaps you meant 'table_c' instead of 'table_b'.","message":"Could not find a relationship between 'table_a' and 'table_b' in the schema cache"}
```

In a Next.js app using `@supabase/ssr`, this surfaces as a silent 404 — the server component calls `notFound()` because `supabase.from(...).select(...).single()` returns an error or null.

## Root Cause

PostgREST (the REST API layer behind `supabase-js`) resolves relationships between tables **only through direct foreign key constraints**. It does NOT infer transitive relationships through a common third table — even when both tables have foreign keys pointing to the same target.

For example, if:

- `profiles.id` → FK → `auth.users.id`  
- `posts.author_id` → FK → `auth.users.id`

Then `supabase.from("posts").select("*,profiles(display_name)")` will **fail** because there is no direct FK from `posts.author_id` to `profiles.id`. PostgREST cannot deduce "profiles where id equals posts.author_id" through the shared reference to `auth.users`.

## Fix

### 1. Add the missing FK constraint

```sql
ALTER TABLE public.posts 
ADD CONSTRAINT posts_author_id_profiles_fkey 
FOREIGN KEY (author_id) REFERENCES public.profiles(id) 
ON DELETE SET NULL;
```

Use `ON DELETE SET NULL` so deleting a profile does not cascade-delete all their posts.

### 2. Reload the PostgREST schema cache

PostgREST caches the database schema at startup. Adding a FK does not immediately update the cache. Force a reload:

```sql
NOTIFY pgrst, 'reload schema';
```

Or in Supabase Dashboard → SQL Editor, run the NOTIFY command directly.

### 3. Verify

```bash
curl -s -G "https://<project>.supabase.co/rest/v1/posts" \
  -H "apikey: <anon-key>" \
  -H "Authorization: Bearer <anon-key>" \
  --data-urlencode "select=*,profiles(display_name)" \
  --data-urlencode "slug=eq.some-slug"
```

Expected: returns post data with nested `profiles` object (or null for `author_id = NULL`).

## Prevention

When designing a Supabase schema with a `public.profiles` table, ensure every table that references `auth.users.id` via `author_id` also has a **direct FK** to `public.profiles(id)`:

```sql
ALTER TABLE public.posts 
  ADD CONSTRAINT fk_posts_author_profile 
  FOREIGN KEY (author_id) REFERENCES public.profiles(id) 
  ON DELETE SET NULL;
```

The existing FKs to `auth.users` are irrelevant for PostgREST join resolution — only direct table-to-table constraints matter.
