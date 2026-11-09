# miu-auto-tabletonephantom-f — El "DOI" cambia por proceso

> *"# miu-auto-tabletonephantom-f"*
>
> — El README original de este repo (28 B, título solo, sin salto de
> línea final; leído por GitHub 2026-11-09 ~16:15 -05, SHA
> `934ae6dced5809122acc7e9837600495f7c86be7`).
>
> **Decisión de siembra: el título SE CONSERVA**, citado arriba como
> epígrafe. Esta cáscara no tenía tema: se llena con un hecho medido,
> no con investigación web (modelo cipher-0, como
> `miu-auto-cipher19051997-0`, sembrado 2026-11-07).

## El registro

- Repo: `Jaime393/miu-auto-tabletonephantom-f`.
- Antes de la siembra: 1 commit, "Initial commit", 2026-08-25T17:20:11Z,
  autor FranBot-Evolucion. Cáscara, sin desarrollo.
- Siembra: 2026-11-09 ~16:18 -05. Verificado por mí en local, leyendo
  el código en GitHub y reproduciendo en 3 procesos.

## El hecho medido

En `pva-ledger` y en `pva-api`, la función `ledger_publish` construye
el "DOI" con `hash()` de Python sobre un `str`. `hash()` de `str` es
aleatorio por proceso: la misma entrada da un "DOI" distinto en cada
ejecución. El sha256 y el `arweave_tx` no cambian; solo el "DOI".

- `pva-ledger`, `cli.py`, comando `publish` (1.278 B, leído en vivo):
  `doi = f"10.5281/zenodo.{abs(hash(h)) % 10000000}" if zenodo else None`
  — el DOI solo se calcula si se pasa `--zenodo`; si no, es `None`.
- `pva-api`, `app.py`, función `ledger_publish` (5.966 B, leída en
  vivo): `"zenodo_doi": f"10.5281/zenodo.{abs(hash(h))%10000000}"`
  — el DOI se calcula siempre.

Mi reproducción, misma entrada `"prueba-doi-hash"`, 3 procesos
(2026-11-09 ~16:18 -05):

| Proceso | sha256 (primeros 16) | arweave_tx | "DOI" |
|---|---|---|---|
| 1 | `4e06c5e4aaf6b4ac`… | `arweave_tx_4e06c5e4aaf6b4ac` | `10.5281/zenodo.7765607` |
| 2 | `4e06c5e4aaf6b4ac`… | `arweave_tx_4e06c5e4aaf6b4ac` | `10.5281/zenodo.9314582` |
| 3 | `4e06c5e4aaf6b4ac`… | `arweave_tx_4e06c5e4aaf6b4ac` | `10.5281/zenodo.1837178` |

El sha256 completo es idéntico en los 3 procesos
(`4e06c5e4aaf6b4aca9d45ff9c6f8e52c41e77b0f53b3ce73be1500a472f7c947`).
El `arweave_tx` es una cadena local, `arweave_tx_{h[:16]}`: determinista,
no es una transacción. Ninguno de los tres "DOI" existe en Zenodo: el
código no llama a ninguna API de Zenodo (ni `requests`, ni `urllib`, ni
`zenodo.org` en la función).

Mediciones anteriores que convergen (minería ola 4, archivos locales):

- `pva-ledger`, 2026-11-09 ~07:40 -05: misma entrada, 3 procesos →
  4553639, 9651531, 4424841.
- `pva-api`, 2026-11-09 ~07:48 -05: misma entrada, 3 procesos →
  2781851, 8683245, 1163665.

Consecuencia: el mismo contenido publicado dos veces recibe dos "DOI"
distintos. Un "DOI" que cambia en cada ejecución no identifica nada.

## Comprobación

```
python3 doi_hash_repro.py            # 3 procesos, imprime TODO COINCIDE
python3 test_doi_hash.py             # 6 tests
```

`doi_hash_repro.py` contiene la copia literal de `ledger_publish`
(pva-api, app.py) y la variante condicional de pva-ledger (cli.py).
`test_doi_hash.py` comprueba: sha256 idéntico en 3 procesos,
`arweave_tx` idéntico en 3 procesos, DOI distinto en 3 procesos, el
mecanismo `abs(hash(h))` presente en el código copiado, y la variante
de pva-ledger (None sin `--zenodo`, distinto por proceso con `--zenodo`).

## Archivos

- `README.md` — esta semilla.
- `doi_hash_repro.py` — la reproducción (stdlib, sin red, sin claves).
- `test_doi_hash.py` — 6 tests (stdlib, sin red, sin claves).
- `HUESO_DOI_HASH.md` — el hueso: el hecho en una página.
- `EVOLUCION.md` — qué es esta siembra y qué sigue.
- `CARENCIAS.md` — lo NO SÉ (nunca contenido).
