-- Ejecutar una sola vez en Supabase SQL Editor.
-- La fecha corresponde al vencimiento que figura en el certificado de cada unidad.
ALTER TABLE public.unidades
ADD COLUMN IF NOT EXISTS revision_tecnica_vence date;

COMMENT ON COLUMN public.unidades.revision_tecnica_vence IS
'Fecha exacta de vencimiento de la revisión técnica registrada desde el certificado; NULL si no se ha verificado.';
