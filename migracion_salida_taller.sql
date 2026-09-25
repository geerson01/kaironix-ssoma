-- Añadir plazo estimado del taller a una instalación existente.
alter table public.unidades
  add column if not exists fecha_salida_estimada date;

-- Conservar fechas reales de internamiento y registros anteriores.
