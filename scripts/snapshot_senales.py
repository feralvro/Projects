import json, os, sys
carpeta, modelo, salida = sys.argv[1:4]
PUB = ["clearance_relativo","contratos_adquisicion","contratos_ancla","drop_semanal","propietarios_atendidos","open_cierre","margen_contribucion","listados_7d","recortes_propios","recorte_medio_casa","ventas_salida","lag_cierre","fuera_web","opciones_open"]
QUITAR = {"notas","porque","nota_ultima_lectura","formato"}
def limpiar(d):
    o = {}
    for k, v in d.items():
        if k in QUITAR: continue
        if k == "puntos" and isinstance(v, list):
            o[k] = [{a: b for a, b in p.items() if not (isinstance(b, str) and len(b) > 100)} for p in v]
        else: o[k] = v
    return o
res = {}
for s in PUB:
    p = os.path.join(carpeta, s + ".json")
    if os.path.exists(p): res[s] = limpiar(json.load(open(p, encoding="utf-8")))
    else: print("aviso: falta", s)
os.makedirs(salida, exist_ok=True)
json.dump(res, open(os.path.join(salida, "senales.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
json.dump(json.load(open(modelo, encoding="utf-8")), open(os.path.join(salida, "modelo.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
