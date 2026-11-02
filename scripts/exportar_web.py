#!/usr/bin/env python3
"""
Genera los ficheros de datos de la web pública a partir de lo que el contador ya
publica cada día en el repositorio (data/panel.json y data/dias/*.json).

    python3 scripts/exportar_web.py            # desde la raíz del repo
    python3 scripts/exportar_web.py --datos data --salida web/data

Qué hace (y por qué):
  * panel.json  -> web/data/panel.json, sin el número de parcela ni el de escritura de cada
                   venta (la página nunca los muestra). Los números de documento de
                   Home Loans SÍ se conservan porque la página los enseña.
  * dias/*.json -> web/data/dias.json, un solo fichero. Todos los días menos el
                   último van reducidos a los campos que la página usa; así el
                   fichero crece poco aunque pasen los meses.
  * senales.json y modelo.json NO se tocan: son instantáneas que se actualizan
                   aparte (las escribe quien hace el barrido semanal).
Solo usa la biblioteca estándar.
"""
import argparse
import glob
import json
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--datos", default="data")
ap.add_argument("--salida", default="web/data")
ap.add_argument("--ocultar-documentos", action="store_true")
a = ap.parse_args()

os.makedirs(a.salida, exist_ok=True)


def cargar(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def guardar(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, path)


# ---------- panel ----------
panel_path = os.path.join(a.datos, "panel.json")
if not os.path.exists(panel_path):
    sys.exit("No encuentro %s" % panel_path)
panel = cargar(panel_path)
if not panel.get("inventario"):
    sys.exit("panel.json no trae 'inventario': no publico nada")

mar = (panel.get("registros") or {}).get("maricopa") or {}
for v in (mar.get("ventas_emparejadas") or {}).get("lista", []) or []:
    for k in ("apn", "venta_escritura"):
        v.pop(k, None)
if a.ocultar_documentos:  # opcional: la página muestra estos números tal cual, así que por defecto se conservan
    for v in (mar.get("hipotecas_ohl") or {}).get("lista", []) or []:
        v.pop("rn", None)
guardar(os.path.join(a.salida, "panel.json"), panel)

# ---------- dias ----------
ficheros = sorted(glob.glob(os.path.join(a.datos, "dias", "*.json")))
if not ficheros:
    sys.exit("No hay data/dias/*.json: no publico nada")
dias = [cargar(f) for f in ficheros]
dias = [d for d in dias if d.get("fecha") and d.get("total")]
dias.sort(key=lambda d: d["fecha"])


def reducido(d):
    p = d.get("precios") or {}
    c = d.get("clasificacion") or {}
    out = {k: d.get(k) for k in ("fecha", "total", "nuevos", "retirados", "reapariciones", "primera_pasada",
                                 "valor_salido_hoy", "valor_salido_hoy_base") if d.get(k) is not None}
    out["precios"] = {k: p.get(k) for k in ("precio_mediana", "cobertura_pct", "recortes_hoy", "recorte_medio_hoy_pct")
                      if p.get(k) is not None}
    if c.get("en_venta_estimadas"):
        out["clasificacion"] = {"en_venta_estimadas": c["en_venta_estimadas"]}
    return out


salida = [reducido(d) for d in dias[:-1]] + [dias[-1]]  # el último día va completo
guardar(os.path.join(a.salida, "dias.json"), salida)

print("OK  panel generado=%s  dias=%d  ultimo=%s" % (panel.get("generado"), len(salida), dias[-1]["fecha"]))
