# Carencias — miu-auto-tabletonephantom-f

Lo NO SÉ de esta siembra. No es contenido: son huecos míos, locales,
con dónde se buscó y fecha. Nada de esto se afirma en el README ni en
el hueso.

1. **NO SÉ si alguno de los "DOI" generados por `ledger_publish` se
   registró alguna vez en Zenodo.** Dónde se buscó: el código de
   `pva-ledger/cli.py` y `pva-api/app.py` no llama a ninguna API de
   Zenodo (leído en vivo 2026-11-09 ~16:15 -05), así que el código no
   puede producir un DOI real. Pero si alguien registró uno a mano en
   Zenodo, eso no está en el código y no se comprobó (no se consultó
   Zenodo). Fecha: 2026-11-09.
2. **NO SÉ si el comando `publish` de pva-ledger se ejecutó alguna
   vez con `--zenodo`.** Dónde se buscó: el repo no tiene logs ni
   registros de ejecución (minería ola 4, tanda 2). Fecha: 2026-11-09.
3. **NO SÉ si el endpoint `POST /api/publish` de pva-api se llamó
   alguna vez.** Dónde se buscó: el repo no tiene logs; el código
   escribe un log fuera del repo
   (`~/miu-ecosistema/data/micelio_log.jsonl`) solo para `/api/micelio`,
   no para `/api/publish` (leído en `app.py` 2026-11-09 ~16:15 -05).
   Fecha: 2026-11-09.
4. **NO SÉ qué versión exacta de Python corre el `hash()` medido.**
   Dónde se buscó: el Dockerfile de pva-ledger fija `python:3.11-slim`
   (minería ola 4, tanda 2); mis 3 procesos corrieron con el Python 3
   de esta VM. El defecto (hash de `str` aleatorio por proceso) es el
   comportamiento documentado de CPython con la sal por proceso, y la
   reproducción en 3 procesos lo confirma en esta VM; en otra versión
   el número cambia, el mecanismo no. Fecha: 2026-11-09.
5. **NO SÉ si existe otra copia de `ledger_publish` en más repos.**
   Dónde se buscó: la búsqueda de código en GitHub por
   `ledger_publish` en `pva-ledger` y `pva-api` devolvió 0 resultados
   (el índice de búsqueda no cubre estos repos); la minería de la ola 4
   encontró la función en esos dos repos y en ningún otro de los 10 de
   la ola. Fuera de la ola 4 no se buscó. Fecha: 2026-11-09.
