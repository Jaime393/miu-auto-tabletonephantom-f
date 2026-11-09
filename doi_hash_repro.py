#!/usr/bin/env python3
"""Reproduce el defecto del "DOI" de ledger_publish (pva-ledger y pva-api).

La función es copia literal de Jaime393/pva-api, app.py, función
ledger_publish — leída en vivo por GitHub 2026-11-09 ~16:15 -05.
Solo stdlib. No se modificó nada de la función copiada.

La variante de Jaime393/pva-ledger, cli.py, comando publish, es la misma
línea con una condición: el DOI solo se calcula si se pasa --zenodo
(doi = ... if zenodo else None). Se reproduce también, abajo.

Hecho medido: con la MISMA entrada, en 3 procesos distintos, el sha256
y el arweave_tx son idénticos, y el "DOI" es distinto en cada proceso.
El DOI se construye con hash() de Python sobre un str, y hash() de str
es aleatorio por proceso (la sal cambia en cada ejecución).

Uso: python3 doi_hash_repro.py [entrada]
Sin argumento usa "prueba-doi-hash".
Salida 0 si la reproducción confirma el defecto; 1 si no.
"""

import hashlib
import datetime
import json
import subprocess
import sys

# Copia literal de ledger_publish (pva-api, app.py). Solo stdlib.
def ledger_publish(c):
    h = hashlib.sha256(c.encode()).hexdigest()
    return {"sha256": h, "arweave_tx": f"arweave_tx_{h[:16]}",
            "zenodo_doi": f"10.5281/zenodo.{abs(hash(h)) % 10000000}",
            "timestamp": datetime.datetime.now().isoformat()}


def doi_ledger(h, zenodo):
    """Variante pva-ledger (cli.py, comando publish): DOI solo con --zenodo."""
    return f"10.5281/zenodo.{abs(hash(h)) % 10000000}" if zenodo else None


def correr_una_vez(entrada):
    """Ejecuta ledger_publish en un proceso nuevo y devuelve su salida."""
    codigo = (
        "import hashlib, json, sys; "
        "h = hashlib.sha256(sys.argv[1].encode()).hexdigest(); "
        "print(json.dumps({'sha256': h, "
        "'arweave_tx': f'arweave_tx_{h[:16]}', "
        "'zenodo_doi': f\"10.5281/zenodo.{abs(hash(h)) % 10000000}\"}))"
    )
    r = subprocess.run([sys.executable, "-c", codigo, entrada],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "prueba-doi-hash"
    print("Entrada:", repr(entrada))
    print("Función: ledger_publish, copia literal de pva-api/app.py")
    resultados = [correr_una_vez(entrada) for _ in range(3)]
    for i, r in enumerate(resultados, 1):
        print(f"Proceso {i}: sha256={r['sha256'][:16]}... "
              f"arweave_tx={r['arweave_tx']} doi={r['zenodo_doi']}")
    sha_iguales = len({r["sha256"] for r in resultados}) == 1
    tx_iguales = len({r["arweave_tx"] for r in resultados}) == 1
    doi_distintos = len({r["zenodo_doi"] for r in resultados})
    print(f"sha256 idéntico en los 3 procesos: {sha_iguales}")
    print(f"arweave_tx idéntico en los 3 procesos: {tx_iguales}")
    print(f"DOI distintos en 3 procesos: {doi_distintos}")
    # Variante pva-ledger: sin --zenodo el DOI es None.
    h = hashlib.sha256(entrada.encode()).hexdigest()
    print(f"Variante pva-ledger sin --zenodo: {doi_ledger(h, False)}")
    print(f"Variante pva-ledger con --zenodo: {doi_ledger(h, True)}")
    if sha_iguales and tx_iguales and doi_distintos == 3:
        print("TODO COINCIDE: el DOI cambia por proceso; el resto no.")
        return 0
    print("NO COINCIDE: el defecto no se reprodujo en esta corrida.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
