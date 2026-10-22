# Full Migration Template

A complete Supabase migration template covering base tables, feature-specific tables, RLS, triggers, seed data, and indexes.

Structure (in order):
1. Base tables (profiles, categories, posts, comments, likes)
2. Feature-specific tables (tags, faces, reports, entities)
3. RLS enable
4. RLS policies for all tables
5. Triggers (auto-profile, counter updates)
6. Seed data
7. Extensions (pg_trgm)
8. Indexes

Key patterns:

- All tables use `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- Timestamps use `TIMESTAMPTZ DEFAULT NOW()`
- Auth user references: `REFERENCES auth.users(id) ON DELETE CASCADE`
- RLS pattern: public read, auth insert, admin write
- Many-to-many junction tables use `UNIQUE(field_a, field_b)`
- Auto-increment counters via AFTER INSERT OR DELETE triggers
- Full-text search with GIN indexes on title and content
- pg_trgm GIN indexes for fuzzy search on text fields

See the full migration at: ~/theliems/scripts/004_full_migration.sql (24835 bytes, 10 tables, 10 scam tags seed)
