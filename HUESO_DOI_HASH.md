# Hueso — El "DOI" cambia por proceso

**Hecho:** en `pva-ledger` y en `pva-api`, la función `ledger_publish`
construye el "DOI" con `hash()` de Python sobre un `str`. `hash()` de
`str` es aleatorio por proceso. La misma entrada da un "DOI" distinto
en cada ejecución. El sha256 y el `arweave_tx` no cambian; solo el
"DOI". Un "DOI" que cambia en cada ejecución no identifica nada.

**Fuente y fecha:**

- `Jaime393/pva-ledger`, `cli.py` (1.278 B), comando `publish`, leído
  en vivo por GitHub 2026-11-09 ~16:15 -05:
  `doi = f"10.5281/zenodo.{abs(hash(h)) % 10000000}" if zenodo else None`
- `Jaime393/pva-api`, `app.py` (5.966 B), función `ledger_publish`,
  leída en vivo por GitHub 2026-11-09 ~16:15 -05:
  `"zenodo_doi": f"10.5281/zenodo.{abs(hash(h))%10000000}"`
- Reproducción propia, 2026-11-09 ~16:18 -05, entrada
  `"prueba-doi-hash"`, 3 procesos: sha256 idéntico
  (`4e06c5e4aaf6b4aca9d45ff9c6f8e52c41e77b0f53b3ce73be1500a472f7c947`),
  `arweave_tx` idéntico (`arweave_tx_4e06c5e4aaf6b4ac`), "DOI"
  distintos: 7765607, 9314582, 1837178.
- Mediciones anteriores que convergen (minería ola 4):
  `pva-ledger`, 2026-11-09 ~07:40 -05: 4553639, 9651531, 4424841;
  `pva-api`, 2026-11-09 ~07:48 -05: 2781851, 8683245, 1163665.

**Precisiones:**

- En `pva-ledger` el DOI solo se calcula si se pasa `--zenodo`; si
  no, es `None`. En `pva-api` se calcula siempre.
- El `arweave_tx` es una cadena local, `arweave_tx_{h[:16]}`:
  determinista, no es una transacción.
- Ninguno de los "DOI" medidos existe en Zenodo: el código no llama
  a ninguna API de Zenodo (ni `requests`, ni `urllib`, ni `zenodo.org`
  en la función).
- El mismo contenido publicado dos veces recibe dos "DOI" distintos.

**Comprobación:** `python3 doi_hash_repro.py` (salida 0),
`python3 test_doi_hash.py` (6 tests).
