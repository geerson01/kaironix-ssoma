-- Ejecutar una sola vez en Supabase SQL Editor antes de usar la opción En taller.
alter table public.unidades
  add column if not exists diagnostico_taller text;

alter table public.unidades
  add column if not exists fecha_internamiento date;

-- No modifica inspecciones históricas ni el estado de las unidades existentes.
