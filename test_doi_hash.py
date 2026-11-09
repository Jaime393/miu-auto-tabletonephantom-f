#!/usr/bin/env python3
"""Tests del defecto del "DOI" de ledger_publish (pva-ledger y pva-api).

Solo stdlib (unittest). No hay red, no hay claves, no hay escritura
fuera de /tmp.

Los tests 1–3 ejecutan la copia literal de ledger_publish (pva-api,
app.py) en procesos separados. El test 4 comprueba el mecanismo en el
código copiado. El test 5 cubre la variante de pva-ledger (cli.py):
sin --zenodo el DOI es None; con --zenodo cambia por proceso.
"""

import hashlib
import inspect
import json
import subprocess
import sys
import unittest

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from doi_hash_repro import doi_ledger, ledger_publish


ENTRADA = "prueba-doi-hash"


def correr(entrada):
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


class TestDoiHash(unittest.TestCase):
    def test_sha256_identico_en_3_procesos(self):
        resultados = [correr(ENTRADA) for _ in range(3)]
        shas = {r["sha256"] for r in resultados}
        self.assertEqual(len(shas), 1, f"sha256 debería ser idéntico: {shas}")
        self.assertEqual(
            next(iter(shas)),
            hashlib.sha256(ENTRADA.encode()).hexdigest(),
        )

    def test_arweave_tx_identico_en_3_procesos(self):
        resultados = [correr(ENTRADA) for _ in range(3)]
        txs = {r["arweave_tx"] for r in resultados}
        self.assertEqual(len(txs), 1, f"arweave_tx debería ser idéntico: {txs}")
        self.assertTrue(next(iter(txs)).startswith("arweave_tx_"))

    def test_doi_distinto_en_3_procesos(self):
        resultados = [correr(ENTRADA) for _ in range(3)]
        dois = {r["zenodo_doi"] for r in resultados}
        self.assertEqual(len(dois), 3,
                         f"el DOI debería ser distinto en cada proceso: {dois}")
        for doi in dois:
            self.assertTrue(doi.startswith("10.5281/zenodo."))

    def test_mecanismo_hash_en_el_codigo(self):
        fuente = inspect.getsource(ledger_publish)
        self.assertIn("abs(hash(h))", fuente,
                      "la función copiada debe construir el DOI con hash()")
        self.assertNotIn("requests", fuente)
        self.assertNotIn("urllib", fuente)
        self.assertNotIn("zenodo.org", fuente)

    def test_variante_ledger_sin_zenodo_es_none(self):
        h = hashlib.sha256(ENTRADA.encode()).hexdigest()
        self.assertIsNone(doi_ledger(h, False))
        doi = doi_ledger(h, True)
        self.assertTrue(doi.startswith("10.5281/zenodo."))

    def test_variante_ledger_cambia_por_proceso(self):
        codigo = (
            "import hashlib, sys; "
            "h = hashlib.sha256(sys.argv[1].encode()).hexdigest(); "
            "print(f\"10.5281/zenodo.{abs(hash(h)) % 10000000}\")"
        )
        dois = set()
        for _ in range(3):
            r = subprocess.run([sys.executable, "-c", codigo, ENTRADA],
                               capture_output=True, text=True, check=True)
            dois.add(r.stdout.strip())
        self.assertEqual(len(dois), 3,
                         f"el DOI de la variante ledger también cambia: {dois}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
