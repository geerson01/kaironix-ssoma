-- KAIRONIX SSOMA 360
-- Migración del piloto de inspección de implementos.
-- Ejecutar una sola vez en Supabase > SQL Editor > New query.

alter table public.inspecciones
  add column if not exists conos_cantidad integer not null default 0,
  add column if not exists tacos_cantidad integer not null default 0,
  add column if not exists botiquin_estado text,
  add column if not exists extintor_tiene boolean not null default false,
  add column if not exists extintor_anio_vencimiento integer,
  add column if not exists extintor_mes_vencimiento integer,
  add column if not exists porcentaje_cumplimiento integer not null default 0;

alter table public.inspecciones
  drop constraint if exists inspecciones_extintor_mes_check;

alter table public.inspecciones
  add constraint inspecciones_extintor_mes_check
  check (extintor_mes_vencimiento is null or extintor_mes_vencimiento between 1 and 12);

alter table public.inspecciones
  drop constraint if exists inspecciones_porcentaje_cumplimiento_check;

alter table public.inspecciones
  add constraint inspecciones_porcentaje_cumplimiento_check
  check (porcentaje_cumplimiento between 0 and 100);

comment on column public.inspecciones.conos_cantidad is 'Cantidad de conos encontrados; mínimo del piloto: 2';
comment on column public.inspecciones.tacos_cantidad is 'Cantidad de tacos encontrados; mínimo del piloto: 2';
comment on column public.inspecciones.extintor_anio_vencimiento is 'Año visible de vencimiento del extintor';
comment on column public.inspecciones.extintor_mes_vencimiento is 'Mes de vencimiento del extintor, de 1 a 12';
comment on column public.inspecciones.porcentaje_cumplimiento is 'Porcentaje de 0 a 100; cada implemento representa 25 puntos';
