-- Ejecutar una sola vez en el SQL Editor del proyecto kaironix-ssoma.
alter table public.profiles
  add column if not exists username text unique,
  add column if not exists correo_contacto text;

-- Asigna el usuario visible a la cuenta administradora existente.
update public.profiles
set username = 'gllajae',
    correo_contacto = 'geersonllaja10@gmail.com'
where id = '5111c387-7c8f-410a-b560-019fbc234050';

