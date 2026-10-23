-- Run once in the Supabase SQL editor.
-- One row per user holding the whole progress document; row level security
-- makes sure a user can only ever read or write their own row.
create table if not exists public.progress (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  data       jsonb not null,
  updated_at timestamptz not null default now()
);

alter table public.progress enable row level security;

create policy "read own progress" on public.progress
  for select using (auth.uid() = user_id);

create policy "insert own progress" on public.progress
  for insert with check (auth.uid() = user_id);

create policy "update own progress" on public.progress
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "delete own progress" on public.progress
  for delete using (auth.uid() = user_id);
